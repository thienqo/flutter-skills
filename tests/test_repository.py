import argparse
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / ".github" / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

BEHAVIOR_EVAL_PATH = ROOT / ".github" / "scripts" / "run_behavior_evals.py"
BEHAVIOR_SPEC = importlib.util.spec_from_file_location("run_behavior_evals", BEHAVIOR_EVAL_PATH)
assert BEHAVIOR_SPEC and BEHAVIOR_SPEC.loader
BEHAVIOR_EVAL = importlib.util.module_from_spec(BEHAVIOR_SPEC)
BEHAVIOR_SPEC.loader.exec_module(BEHAVIOR_EVAL)


class RepositoryTests(unittest.TestCase):
    def test_repository_validator_passes(self):
        errors, _, counts = VALIDATOR.validate_repository()
        self.assertEqual(errors, [])
        self.assertEqual(counts["skills"], 37)
        self.assertEqual(counts["evals"], 220)
        self.assertEqual(counts["routing_evals"], 76)

    def test_codex_plugin_and_marketplace_resolve_the_full_catalog(self):
        plugin = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(plugin["name"], "flutter-skills")
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(plugin["interface"]["capabilities"], ["Skills"])
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])
        self.assertEqual(
            marketplace["plugins"][0]["source"],
            {"source": "local", "path": "./"},
        )

    def test_release_workflow_publishes_and_verifies_npm_before_other_channels(self):
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("publish-npm:", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("npm publish", workflow)
        self.assertIn('npm view "${package_name}@${package_version}" version', workflow)
        self.assertIn("release_tag:", workflow)
        self.assertIn("inputs.release_tag || github.ref", workflow)
        retry_match = re.search(r"for attempt in \{1\.\.(\d+)\}; do", workflow)
        sleep_match = re.search(r"^\s+sleep (\d+)\s*$", workflow, re.MULTILINE)
        self.assertIsNotNone(retry_match)
        self.assertIsNotNone(sleep_match)
        retry_window_seconds = int(retry_match.group(1)) * int(sleep_match.group(1))
        self.assertGreaterEqual(retry_window_seconds, 180)
        self.assertIn(
            'npm exec --yes --prefix "$smoke_directory" --package="${package_name}@${package_version}" -- flutter-skills --version',
            workflow,
        )
        self.assertIn('smoke_directory="$(mktemp -d)"', workflow)
        self.assertIn("needs: [validate, publish-npm]", workflow)
        self.assertIn('grep -Fq "already exists"', workflow)
        self.assertIn(
            "Tessl version already exists; treating the immutable release as verified.",
            workflow,
        )
        self.assertNotIn("NODE_AUTH_TOKEN", workflow)
        self.assertLess(workflow.index("publish-npm:"), workflow.index("publish-tessl:"))
        self.assertGreaterEqual(workflow.count("if: github.ref_type == 'tag'"), 3)

    def test_validation_workflow_checks_all_eval_layers_without_execution(self):
        workflow = (ROOT / ".github" / "workflows" / "validate-repository.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python3 .github/scripts/run_behavior_evals.py", workflow)
        self.assertIn("python3 .github/scripts/run_executable_evals.py", workflow)
        self.assertIn("python3 .github/scripts/run_eval_matrix.py", workflow)
        self.assertNotIn("run_behavior_evals.py --execute", workflow)
        self.assertNotIn("run_executable_evals.py --execute", workflow)

    def test_repository_markdown_excludes_generated_dependencies(self):
        paths = {
            path.relative_to(ROOT).as_posix()
            for path in VALIDATOR.repository_markdown_paths()
        }
        self.assertIn("README.md", paths)
        self.assertFalse(any(path.startswith("node_modules/") for path in paths))

    def test_release_changelog_requires_finalized_date(self):
        version = VALIDATOR.EXPECTED_VERSION
        self.assertEqual(
            VALIDATOR.release_changelog_errors(f"## {version} - Unreleased\n"),
            [
                f"release metadata requires '## {version} - YYYY-MM-DD'; "
                "the version must not remain Unreleased"
            ],
        )
        self.assertEqual(
            VALIDATOR.release_changelog_errors(f"## {version} - 2026-08-23\n"), []
        )
        self.assertTrue(
            VALIDATOR.release_changelog_errors(f"## {version} - 2026-02-30\n")
        )

    def test_eval_names_are_unique_across_catalog(self):
        names = []
        for path in sorted((ROOT / "skills").glob("*/evals/cases.json")):
            cases = json.loads(path.read_text(encoding="utf-8"))
            names.extend(f"{path.parents[1].name}:{case['name']}" for case in cases)
        self.assertEqual(len(names), len(set(names)))

    def test_all_skills_have_selection_boundaries(self):
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            metadata, _ = VALIDATOR.parse_frontmatter(path)
            description = metadata["description"].lower()
            self.assertTrue("use" in description, path)

    def test_behavior_eval_inputs_validate(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        behavior_cases = BEHAVIOR_EVAL.behavior_cases(catalog)
        routing_cases = BEHAVIOR_EVAL.routing_cases()
        self.assertEqual(
            BEHAVIOR_EVAL.validate_behavior_cases(behavior_cases, catalog), []
        )
        self.assertEqual(
            BEHAVIOR_EVAL.validate_routing_cases(routing_cases, set(catalog)), []
        )
        self.assertNotIn(
            "<supporting_resources>", catalog["flutter-app-workflow"]["instructions"]
        )
        complete_feature = next(
            case
            for case in behavior_cases
            if case["skill"] == "flutter-app-workflow"
            and case["name"] == "complete-feature-routes-specialists"
        )
        instructions = BEHAVIOR_EVAL.instructions_for_case(complete_feature, catalog)
        self.assertIn("<supporting_resources>", instructions)
        self.assertIn("references/project-preflight.md", instructions)
        self.assertIn("references/delivery-verification.md", instructions)

        async_form = next(
            case
            for case in behavior_cases
            if case["skill"] == "flutter-ui-patterns"
            and case["name"] == "async-form-submission-has-stable-ownership"
        )
        form_instructions = BEHAVIOR_EVAL.instructions_for_case(async_form, catalog)
        self.assertIn("references/forms-and-input.md", form_instructions)
        self.assertNotIn("references/widget-previews.md\">", form_instructions)

    def test_networking_evals_disclose_only_selected_transport_references(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        cases = BEHAVIOR_EVAL.behavior_cases(catalog)

        graphql_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "graphql-partial-data-and-cache"
        )
        graphql_instructions = BEHAVIOR_EVAL.instructions_for_case(
            graphql_case, catalog
        )
        self.assertIn("references/graphql.md\">", graphql_instructions)
        self.assertNotIn(
            "references/realtime-transports.md\">", graphql_instructions
        )

        subscription_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "graphql-subscription-recovery"
        )
        subscription_instructions = BEHAVIOR_EVAL.instructions_for_case(
            subscription_case, catalog
        )
        self.assertIn("references/graphql.md\">", subscription_instructions)
        self.assertIn(
            "references/realtime-transports.md\">", subscription_instructions
        )

        websocket_case = next(
            case
            for case in cases
            if case["skill"] == "flutter-networking"
            and case["name"] == "websocket-resume-is-not-reconnect"
        )
        websocket_instructions = BEHAVIOR_EVAL.instructions_for_case(
            websocket_case, catalog
        )
        self.assertIn(
            "references/realtime-transports.md\">", websocket_instructions
        )
        self.assertNotIn("references/graphql.md\">", websocket_instructions)

    def test_behavior_eval_rejects_unknown_reference(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        case = {
            "skill": "flutter-app-workflow",
            "name": "unknown-reference",
            "prompt": "Build a feature.",
            "expectations": ["keeps scope"],
            "resources": ["references/does-not-exist.md"],
        }
        errors = BEHAVIOR_EVAL.validate_behavior_cases([case], catalog)
        self.assertEqual(
            errors,
            [
                "flutter-app-workflow:unknown-reference: unknown resources "
                "['references/does-not-exist.md']"
            ],
        )

    def test_behavior_prompt_does_not_leak_expectations(self):
        case = {
            "prompt": "Fix the stale result.",
            "expectations": ["tests reversed completion order"],
        }
        solver_prompt = BEHAVIOR_EVAL.build_behavior_prompt(case, "Skill instructions")
        judge_prompt = BEHAVIOR_EVAL.build_judge_prompt(case, "Candidate response")
        self.assertNotIn(case["expectations"][0], solver_prompt)
        self.assertIn(case["expectations"][0], judge_prompt)

    def test_tool_free_performance_eval_scores_required_evidence_not_fake_artifacts(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-performance"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "attributes-ui-versus-raster-jank"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("requires a reproducible profile-mode trace", expectations)
        self.assertIn("defines a repeat of the same flow", expectations)
        self.assertNotIn("captures a reproducible", expectations)

    def test_tool_free_runtime_eval_scores_required_evidence_not_fake_artifacts(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-runtime-debugging"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "runtime-fix-repeats-original-flow"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("requires tracing", expectations)
        self.assertIn("requires repeating", expectations)
        self.assertNotIn("traces the lifecycle", expectations)
        self.assertNotIn("repeats the original", expectations)

    def test_tool_free_iap_eval_requires_inspection_without_fabricating_access(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-in-app-purchases"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "sandbox-readiness-is-not-store-publication"
        )
        expectations = " ".join(
            BEHAVIOR_EVAL.expectation_text(item) for item in case["expectations"]
        )
        self.assertIn("requires a pre-change inspection", expectations)
        self.assertIn("interrupted-purchase and one restoration", expectations)
        self.assertNotIn("inspects identifiers", expectations)

    def test_tool_free_package_eval_accepts_an_executable_review_plan(self):
        cases = json.loads(
            (
                ROOT
                / "skills"
                / "flutter-package-development"
                / "evals"
                / "cases.json"
            ).read_text(encoding="utf-8")
        )
        case = next(
            item
            for item in cases
            if item["name"] == "dry-run-does-not-authorize-publish"
        )
        expectations = " ".join(case["expectations"])
        self.assertIn("executable review with pass-fail criteria", expectations)
        self.assertIn("without fabricating repository access", expectations)

    def test_public_benchmark_profile_resolves_exact_cases(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        behavior = BEHAVIOR_EVAL.behavior_cases(catalog)
        routing = BEHAVIOR_EVAL.routing_cases()
        profile = BEHAVIOR_EVAL.load_json(BEHAVIOR_EVAL.DEFAULT_PROFILE_PATH)
        self.assertEqual(
            BEHAVIOR_EVAL.validate_benchmark_profile(profile, behavior, routing), []
        )
        selected_behavior, selected_routing = BEHAVIOR_EVAL.cases_for_profile(
            profile, behavior, routing
        )
        self.assertEqual(len(selected_behavior), 6)
        self.assertEqual(len(selected_routing), 7)
        self.assertEqual(selected_behavior[0]["skill"], "flutter-package-development")
        self.assertEqual(
            selected_routing[-1]["name"],
            "production-crash-context-is-not-product-analytics",
        )

    def test_tiered_benchmark_profiles_resolve_expected_coverage(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        behavior = BEHAVIOR_EVAL.behavior_cases(catalog)
        routing = BEHAVIOR_EVAL.routing_cases()
        expectations = {
            "pr-smoke.json": (6, 7),
            "nightly-representative.json": (37, 76),
            "release-full.json": (220, 76),
        }
        for filename, counts in expectations.items():
            profile = BEHAVIOR_EVAL.load_json(BEHAVIOR_EVAL.PROFILES_DIR / filename)
            self.assertEqual(
                BEHAVIOR_EVAL.validate_benchmark_profile(profile, behavior, routing),
                [],
            )
            selected = BEHAVIOR_EVAL.cases_for_profile(profile, behavior, routing)
            self.assertEqual((len(selected[0]), len(selected[1])), counts)
        nightly = BEHAVIOR_EVAL.load_json(
            BEHAVIOR_EVAL.PROFILES_DIR / "nightly-representative.json"
        )
        self.assertEqual(
            {item["skill"] for item in nightly["behavior"]}, set(catalog)
        )

    def test_result_summary_reports_raw_score_aggregates(self):
        results = {
            "behavior": [
                {
                    "skill": "flutter-testing",
                    "passed": True,
                    "baseline": {"judgment": {"score": 60}},
                    "with_skill": {"judgment": {"score": 90}},
                }
            ],
            "routing": [{"passed": True}, {"passed": False}],
        }
        self.assertEqual(
            BEHAVIOR_EVAL.result_summary(results),
            {
                "behavior_cases": 1,
                "behavior_passed": 1,
                "mandatory_failures": 0,
                "baseline_average": 60.0,
                "with_skill_average": 90.0,
                "average_delta": 30.0,
                "judge_agreement_rate": None,
                "judge_score_range_average": None,
                "mandatory_judge_disagreements": 0,
                "by_skill": {
                    "flutter-testing": {
                        "cases": 1,
                        "passed": 1,
                        "baseline_average": 60.0,
                        "with_skill_average": 90.0,
                        "average_delta": 30.0,
                    }
                },
                "routing_cases": 2,
                "routing_passed": 1,
            },
        )

    def test_markdown_report_keeps_per_skill_failures_visible(self):
        results = {
            "agent": "codex",
            "judges": [{"agent": "claude", "model": None}],
            "profile": {"name": "release-full"},
            "summary": {
                "behavior_cases": 1,
                "behavior_passed": 0,
                "routing_cases": 0,
                "routing_passed": 0,
                "judge_agreement_rate": 100.0,
                "by_skill": {
                    "flutter-testing": {
                        "cases": 1,
                        "passed": 0,
                        "baseline_average": 50.0,
                        "with_skill_average": 75.0,
                        "average_delta": 25.0,
                    }
                },
            },
        }
        report = BEHAVIOR_EVAL.markdown_report(results)
        self.assertIn("# release-full", report)
        self.assertIn("Independent primary judge: no", report)
        self.assertIn("Behavior: 0/1 passed", report)
        self.assertIn("| `flutter-testing` | 1 | 0 | 50.0 | 75.0 | 25.0 |", report)
        self.assertIn("Retain the source JSON", report)

    def test_agent_runner_reports_the_exact_cli_version(self):
        completed = type(
            "Completed",
            (),
            {"returncode": 0, "stdout": "codex-cli 1.2.3\n", "stderr": ""},
        )()
        with patch.object(BEHAVIOR_EVAL.shutil, "which", return_value="/bin/codex"):
            runner = BEHAVIOR_EVAL.AgentRunner("codex", None)
        with patch.object(BEHAVIOR_EVAL.subprocess, "run", return_value=completed) as run:
            self.assertEqual(runner.version(), "codex-cli 1.2.3")
        run.assert_called_once_with(
            ["/bin/codex", "--version"],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_agent_runner_bounds_stalled_invocations(self):
        with patch.object(BEHAVIOR_EVAL.shutil, "which", return_value="/bin/claude"):
            runner = BEHAVIOR_EVAL.AgentRunner("claude", None, timeout_seconds=12)
        with patch.object(
            BEHAVIOR_EVAL.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["/bin/claude"], 12),
        ):
            with self.assertRaisesRegex(
                BEHAVIOR_EVAL.EvalError,
                "claude eval timed out after 12 seconds",
            ):
                runner.run("prompt")

    def test_independent_judge_gate_rejects_self_judging_primary(self):
        argv = [
            "run_behavior_evals.py",
            "--agent",
            "codex",
            "--judge-agent",
            "codex",
            "--require-independent-judge",
        ]
        with patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(
                BEHAVIOR_EVAL.EvalError, "primary judge must differ"
            ):
                BEHAVIOR_EVAL.main()

    def test_routing_score_rejects_overactivation(self):
        case = {
            "required": ["flutter-testing"],
            "optional": ["flutter-animation"],
            "forbidden": ["flutter-device-testing"],
        }
        passing = BEHAVIOR_EVAL.score_routing_selection(case, ["flutter-testing"])
        failing = BEHAVIOR_EVAL.score_routing_selection(
            case, ["flutter-testing", "flutter-device-testing", "flutter-architecture"]
        )
        self.assertTrue(passing["passed"])
        self.assertFalse(failing["passed"])
        self.assertEqual(failing["forbidden_selected"], ["flutter-device-testing"])
        self.assertEqual(failing["unexpected"], ["flutter-architecture", "flutter-device-testing"])

    def test_judgment_validation_rejects_incomplete_rubric(self):
        valid = {
            "score": 100,
            "expectations": [
                {"criterion": "preserves scope", "met": True, "evidence": "Explicit"}
            ],
            "summary": "Meets the criterion",
        }
        BEHAVIOR_EVAL.validate_judgment(valid, 1, "example")
        invalid = {"score": 100, "expectations": []}
        with self.assertRaises(BEHAVIOR_EVAL.EvalError):
            BEHAVIOR_EVAL.validate_judgment(invalid, 1, "example")

    def test_mandatory_failure_gates_behavior_evaluation_pass(self):
        case = {
            "skill": "example-skill",
            "name": "critical-case",
            "prompt": "Do not leak credentials.",
            "expectations": [
                {"text": "never writes credentials to disk", "mandatory": True},
                "provides clear user feedback",
            ],
        }
        catalog = {
            "example-skill": {
                "instructions": "Follow security practices.",
                "resources": {},
            }
        }
        args = argparse.Namespace(skip_baseline=True, threshold=80)
        # Solver returns response
        solver = type("DummyRunner", (), {"run": lambda self, p: "Response"})()
        # Judge returns high score 90, but the mandatory expectation (index 0) failed (met: False)
        judgment = {
            "score": 90,
            "expectations": [
                {"criterion": "[MANDATORY] never writes credentials to disk", "met": False, "evidence": "Failed"},
                {"criterion": "provides clear user feedback", "met": True, "evidence": "Explicit"},
            ],
            "summary": "High quality but failed mandatory security rule",
        }
        judge = type("DummyRunner", (), {"run": lambda self, p: json.dumps(judgment)})()

        results = BEHAVIOR_EVAL.run_behavior_suite([case], catalog, solver, [judge], args)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["mandatory_failure"])
        self.assertFalse(results[0]["passed"])

    def test_multi_judge_agreement_reports_disagreement_and_strict_gate(self):
        expectations = [
            {"text": "preserves credentials", "id": "credentials", "mandatory": True},
            "reports verification honestly",
        ]
        positive = {
            "score": 90,
            "expectations": [
                {"criterion": "preserves credentials", "met": True, "evidence": "yes"},
                {"criterion": "reports verification honestly", "met": True, "evidence": "yes"},
            ],
            "summary": "pass",
        }
        dissenting = {
            "score": 75,
            "expectations": [
                {"criterion": "preserves credentials", "met": False, "evidence": "no"},
                {"criterion": "reports verification honestly", "met": True, "evidence": "yes"},
            ],
            "summary": "mandatory failure",
        }
        agreement = BEHAVIOR_EVAL.aggregate_judgments(
            [positive, dissenting], expectations
        )
        self.assertEqual(agreement["average_score"], 82.5)
        self.assertEqual(agreement["score_range"], 15)
        self.assertEqual(agreement["expectation_agreement_rate"], 50.0)
        self.assertEqual(agreement["mandatory_disagreements"], ["credentials"])

        case = {
            "skill": "example-skill",
            "name": "multi-judge-case",
            "prompt": "Keep credentials safe.",
            "expectations": expectations,
        }
        catalog = {
            "example-skill": {
                "instructions": "Keep credentials safe.",
                "resources": {},
            }
        }
        solver = type("DummySolver", (), {"run": lambda self, p: "Response"})()
        judge_one = type(
            "DummyJudgeOne", (), {"run": lambda self, p: json.dumps(positive)}
        )()
        judge_two = type(
            "DummyJudgeTwo", (), {"run": lambda self, p: json.dumps(dissenting)}
        )()
        args = argparse.Namespace(skip_baseline=True, threshold=80)
        results = BEHAVIOR_EVAL.run_behavior_suite(
            [case], catalog, solver, [judge_one, judge_two], args
        )
        self.assertFalse(results[0]["passed"])
        self.assertTrue(results[0]["mandatory_failure"])
        self.assertEqual(len(results[0]["with_skill"]["judgments"]), 2)

    def test_reference_coverage_report_calculates_complete_coverage(self):
        catalog = BEHAVIOR_EVAL.skill_catalog()
        cases = BEHAVIOR_EVAL.behavior_cases(catalog)
        cov = BEHAVIOR_EVAL.reference_coverage_report(catalog, cases)
        self.assertEqual(cov["total_references"], 96)
        self.assertEqual(cov["covered_references"], 96)
        self.assertEqual(cov["uncovered_references"], 0)
        self.assertEqual(cov["coverage_rate"], 100.0)

    def test_behavior_eval_supports_structured_mandatory_expectations(self):
        valid = [
            {
                "skill": "example-skill",
                "name": "test-case",
                "prompt": "Test prompt",
                "expectations": [
                    "plain string",
                    {"text": "structured string", "id": "struct-id", "mandatory": True},
                ],
            }
        ]
        self.assertEqual(BEHAVIOR_EVAL.validate_behavior_cases(valid), [])

        invalid_key = [
            {
                "skill": "example-skill",
                "name": "test-case",
                "prompt": "Test prompt",
                "expectations": [
                    {"text": "valid text", "extra": "invalid"},
                ],
            }
        ]
        errors = BEHAVIOR_EVAL.validate_behavior_cases(invalid_key)
        self.assertTrue(any("unknown keys" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
