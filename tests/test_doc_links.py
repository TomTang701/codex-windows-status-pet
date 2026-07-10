import runpy
import unittest
from pathlib import Path


class DocumentLinkTests(unittest.TestCase):
    def test_internal_markdown_links_are_valid(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_doc_links.py"))
        self.assertEqual(module["check"](), [])


if __name__ == "__main__":
    unittest.main()
