import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / ".github" / "evals" / "behavior" / "flutter-openapi-client" / "fixtures"
HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


class OpenApiFixtureTests(unittest.TestCase):
    def test_json_fixtures_have_unique_operation_ids_and_resolved_local_refs(self):
        for path in sorted(FIXTURES.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(document.get("openapi") or document.get("swagger"), path)

            operation_ids = []
            for path_item in document.get("paths", {}).values():
                for method, operation in path_item.items():
                    if method in HTTP_METHODS:
                        operation_ids.append(operation["operationId"])
            self.assertEqual(len(operation_ids), len(set(operation_ids)), path)

            for reference in self._references(document):
                self.assertTrue(reference.startswith("#/"), (path, reference))
                value = document
                for segment in reference[2:].split("/"):
                    value = value[segment.replace("~1", "/").replace("~0", "~")]
                self.assertIsNotNone(value)

    def test_swagger_ui_fixture_is_neutral_and_uses_inline_spec(self):
        text = (FIXTURES / "swagger-ui-init.js").read_text(encoding="utf-8")
        self.assertIn("spec:", text)
        self.assertIn('"openapi": "3.0.3"', text)
        self.assertNotIn("vitadairy", text.lower())
        self.assertNotIn("token", text.lower())

    def _references(self, value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "$ref":
                    yield child
                else:
                    yield from self._references(child)
        elif isinstance(value, list):
            for child in value:
                yield from self._references(child)


if __name__ == "__main__":
    unittest.main()
