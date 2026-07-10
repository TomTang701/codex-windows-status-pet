import runpy
import unittest
from pathlib import Path


class DocumentParityTests(unittest.TestCase):
    def test_bilingual_document_structure_matches(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_doc_parity.py"))
        self.assertEqual(module["check"](Path(__file__).parents[1]), [])


if __name__ == "__main__":
    unittest.main()
