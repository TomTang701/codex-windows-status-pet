import runpy
import unittest
from pathlib import Path


class DocumentManifestTests(unittest.TestCase):
    def test_manifest_is_valid(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_doc_manifest.py"))
        self.assertEqual(module["check"](), [])


if __name__ == "__main__":
    unittest.main()
