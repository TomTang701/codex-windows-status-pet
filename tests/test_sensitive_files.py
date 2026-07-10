import tempfile
import unittest
from pathlib import Path
import runpy


class SensitiveFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_sensitive_files.py"))

    def test_clean_repository_has_no_sensitive_material(self):
        self.assertEqual(self.module["check"](), [])

    def test_sensitive_filename_and_private_key_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text("TOKEN=redacted", encoding="utf-8")
            marker = "-----BEGIN " + "PRIVATE KEY-----"
            (root / "notes.txt").write_text(marker, encoding="utf-8")
            problems = self.module["check"](root)
            self.assertEqual(len(problems), 2)


if __name__ == "__main__":
    unittest.main()
