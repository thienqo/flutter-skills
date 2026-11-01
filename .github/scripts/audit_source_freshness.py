#!/usr/bin/env python3
"""Audit skill source links and the catalog's recorded verification age."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
POLICY_PATH = ROOT / ".github" / "evals" / "source-freshness-policy.json"
URL_PATTERN = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_source_urls(paths: Iterable[Path]) -> dict[str, list[str]]:
    locations: dict[str, list[str]] = {}
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        for url in URL_PATTERN.findall(path.read_text(encoding="utf-8")):
            locations.setdefault(url, []).append(relative)
    return {url: sorted(set(files)) for url, files in sorted(locations.items())}


GET_FALLBACK_STATUSES = {404, 405}


def classify_status(status: int | None, error: str | None = None) -> str:
    if status is not None and 200 <= status < 400:
        return "ok"
    if status in {401, 403, 429}:
        return "restricted"
    if status in {404, 410}:
        return "broken"
    return "error" if error or status is not None else "error"


def check_url(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "flutter-skills-source-audit/0.2"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            final_url = response.geturl()
            return {
                "url": url,
                "status": status,
                "state": classify_status(status),
                "final_url": final_url,
                "error": None,
            }
    except urllib.error.HTTPError as error:
        # Some servers (support.google.com) answer HEAD with 404 or 405 while
        # GET succeeds, so confirm those codes with a one-byte GET.
        if error.code in GET_FALLBACK_STATUSES:
            get_request = urllib.request.Request(
                url,
                method="GET",
                headers={
                    "User-Agent": "flutter-skills-source-audit/0.2",
                    "Range": "bytes=0-0",
                },
            )
            try:
                with urllib.request.urlopen(get_request, timeout=timeout) as response:
                    status = response.status
                    return {
                        "url": url,
                        "status": status,
                        "state": classify_status(status),
                        "final_url": response.geturl(),
                        "error": None,
                    }
            except (urllib.error.URLError, TimeoutError, OSError) as get_error:
                status = getattr(get_error, "code", None)
                message = str(get_error)
                return {
                    "url": url,
                    "status": status,
                    "state": classify_status(status, message),
                    "final_url": None,
                    "error": message,
                }
        message = str(error)
        return {
            "url": url,
            "status": error.code,
            "state": classify_status(error.code, message),
            "final_url": None,
            "error": message,
        }
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        message = str(error)
        return {
            "url": url,
            "status": None,
            "state": classify_status(None, message),
            "final_url": None,
            "error": message,
        }


def verification_age(policy: dict[str, Any], today: dt.date) -> tuple[int, bool]:
    verified_at = dt.date.fromisoformat(policy["verified_at"])
    age_days = (today - verified_at).days
    return age_days, age_days > int(policy["max_age_days"])


def build_report(
    policy: dict[str, Any],
    locations: dict[str, list[str]],
    checks: list[dict[str, Any]],
    today: dt.date,
) -> dict[str, Any]:
    age_days, stale = verification_age(policy, today)
    entries = []
    for check in checks:
        entries.append({**check, "files": locations[check["url"]]})
    counts = {
        state: sum(entry["state"] == state for entry in entries)
        for state in ("ok", "restricted", "broken", "error")
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "policy": policy,
        "verification_age_days": age_days,
        "verification_stale": stale,
        "unique_urls": len(entries),
        "counts": counts,
        "entries": entries,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("source-freshness.json"))
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--fail-on-broken", action="store_true")
    parser.add_argument("--fail-on-stale", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.timeout <= 0 or args.workers < 1:
        print("ERROR: timeout and workers must be positive", file=sys.stderr)
        return 2
    policy = load_policy()
    paths = sorted(SKILLS_DIR.glob("**/*.md"))
    locations = collect_source_urls(paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        checks = list(
            executor.map(
                lambda url: check_url(url, args.timeout),
                locations,
            )
        )
    report = build_report(policy, locations, checks, dt.date.today())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Audited {report['unique_urls']} source URLs: "
        f"{report['counts']['ok']} ok, {report['counts']['restricted']} restricted, "
        f"{report['counts']['broken']} broken, {report['counts']['error']} errors; "
        f"verification age {report['verification_age_days']} days."
    )
    failed = (
        args.fail_on_broken and report["counts"]["broken"] > 0
    ) or (args.fail_on_stale and report["verification_stale"])
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
