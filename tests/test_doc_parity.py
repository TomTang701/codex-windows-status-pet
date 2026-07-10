import runpy
import json
import tempfile
import unittest
from pathlib import Path


class DocumentParityTests(unittest.TestCase):
    def test_bilingual_document_structure_matches(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_doc_parity.py"))
        self.assertEqual(module["check"](Path(__file__).parents[1]), [])

    def test_semantic_api_drift_is_detected(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_doc_parity.py"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            manifest = {"schema_version": 1, "documents": [{
                "id": "PAIR", "canonical": "a.md", "translations": {"zh-CN": "b.md"}
            }]}
            (root / "docs" / "document_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            prefix = "---\ndocument_version: 1.0.0\n---\n# H\n"
            (root / "a.md").write_text(prefix + "DisplayGeometryAPI\n", encoding="utf-8")
            (root / "b.md").write_text(prefix + "WindowSizeAPI\n", encoding="utf-8")
            errors = module["check"](root)
            self.assertTrue(any("api_names differs" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
