import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from check_doc_navigation import check


class DocumentNavigationTests(unittest.TestCase):
    def fixture(self, root, english_text, chinese_text):
        (root / "docs").mkdir()
        (root / "README.md").write_text(english_text, encoding="utf-8")
        (root / "README.zh-CN.md").write_text(chinese_text, encoding="utf-8")
        (root / "docs" / "document_manifest.json").write_text(
            json.dumps({"documents": [{
                "id": "README",
                "canonical": "README.md",
                "translations": {"zh-CN": "README.zh-CN.md"},
            }]}),
            encoding="utf-8",
        )

    def test_accepts_reciprocal_switches_and_untranslated_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(
                root,
                "# English\n\n简体中文: [中文版本](README.zh-CN.md)\n\n[Archive](docs/archive.md)\n",
                "# 中文\n\nEnglish: [English version](README.md)\n\n[Archive](docs/archive.md)\n",
            )
            (root / "docs" / "archive.md").write_text("# Archive\n", encoding="utf-8")
            self.assertEqual(check(root), [])

    def test_rejects_missing_switch_and_wrong_language_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(
                root,
                "# English\n\n[Wrong language](README.zh-CN.md)\n",
                "# 中文\n\n",
            )
            errors = check(root)
            self.assertTrue(any("missing English-to-Chinese switch" in error for error in errors))
            self.assertTrue(any("missing Chinese-to-English switch" in error for error in errors))
            self.assertTrue(any("wrong-language" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
