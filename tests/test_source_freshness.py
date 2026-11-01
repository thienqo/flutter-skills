import datetime as dt
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / ".github" / "scripts" / "audit_source_freshness.py"
SPEC = importlib.util.spec_from_file_location("audit_source_freshness", SCRIPT_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class SourceFreshnessTests(unittest.TestCase):
    def test_collect_source_urls_deduplicates_and_tracks_files(self):
        paths = [
            ROOT / "skills" / "flutter-performance" / "SKILL.md",
            ROOT / "skills" / "flutter-performance" / "references" / "profile-and-frame-analysis.md",
        ]
        urls = AUDIT.collect_source_urls(paths)
        self.assertIn("https://docs.flutter.dev/perf", urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(
            all(file.startswith("skills/flutter-performance/") or file == "skills/flutter-performance/SKILL.md" for file in urls["https://docs.flutter.dev/perf"])
        )

    def test_status_classification_distinguishes_access_from_breakage(self):
        self.assertEqual(AUDIT.classify_status(200), "ok")
        self.assertEqual(AUDIT.classify_status(302), "ok")
        self.assertEqual(AUDIT.classify_status(403, "forbidden"), "restricted")
        self.assertEqual(AUDIT.classify_status(429, "rate limited"), "restricted")
        self.assertEqual(AUDIT.classify_status(404, "missing"), "broken")
        self.assertEqual(AUDIT.classify_status(None, "timeout"), "error")

    def test_head_404_is_confirmed_with_get(self):
        from unittest import mock
        import urllib.error

        class Response:
            status = 200

            def geturl(self):
                return "https://example.test/page"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(request, timeout):
            if request.get_method() == "HEAD":
                raise urllib.error.HTTPError(request.full_url, 404, "Not Found", {}, None)
            return Response()

        with mock.patch.object(AUDIT.urllib.request, "urlopen", fake_urlopen):
            result = AUDIT.check_url("https://example.test/page", 5)
        self.assertEqual(result["state"], "ok")

    def test_verification_policy_becomes_stale_after_limit(self):
        policy = {"verified_at": "2026-08-24", "max_age_days": 90}
        self.assertEqual(
            AUDIT.verification_age(policy, dt.date(2026, 11, 22)), (90, False)
        )
        self.assertEqual(
            AUDIT.verification_age(policy, dt.date(2026, 11, 23)), (91, True)
        )


if __name__ == "__main__":
    unittest.main()
