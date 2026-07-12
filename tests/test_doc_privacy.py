import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from check_doc_privacy import check


class DocumentPrivacyTests(unittest.TestCase):
    def write(self, root, relative, text):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_accepts_repository_and_generic_userprofile_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "README.md",
                "# Guide\n\nUse `codex-windows-status-pet/scripts/`.\n"
                "Settings are under `%USERPROFILE%\\.codex\\app.json`.\n",
            )
            self.assertEqual(check(root), [])

    def test_rejects_local_paths_escape_links_and_retired_launcher_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "README.md",
                "# Guide\n\n"
                "`C:\\Users\\tangz\\workspace`\n"
                "`file:///C:/Users/tangz/workspace`\n"
                "`\\\\host\\share\\workspace`\n"
                "[outside](../../outside.md)\n"
                "Use `启动Codex状态宠物.cmd`.\n",
            )
            errors = check(root, real_user_fragments=())
            self.assertEqual(len(errors), 5)
            self.assertTrue(any("drive-letter" in error for error in errors))
            self.assertTrue(any("file URI" in error for error in errors))
            self.assertTrue(any("UNC" in error for error in errors))
            self.assertTrue(any("escapes repository" in error for error in errors))
            self.assertTrue(any("retired launcher" in error for error in errors))

    def test_rejects_configured_real_user_fragment_without_rejecting_placeholder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "README.md", "# Guide\n\n<your-user>\nuser tangz\n")
            errors = check(root, real_user_fragments=("tangz",))
            self.assertEqual(len(errors), 1)
            self.assertIn("real-user fragment", errors[0])


if __name__ == "__main__":
    unittest.main()
