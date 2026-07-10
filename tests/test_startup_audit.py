import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from startup_audit import audit_startup, is_legacy_value


class StartupAuditTests(unittest.TestCase):
    def test_known_legacy_entry_is_reported_without_modification(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "Codex Status Pet.lnk").write_text("old", encoding="utf-8")
            result = audit_startup(folder)
            self.assertFalse(result["clean"])
            self.assertEqual(result["legacy_entries"], ["Codex Status Pet.lnk"])
            self.assertTrue((folder / "Codex Status Pet.lnk").exists())

    def test_unrelated_startup_entries_are_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "Ollama.lnk").write_text("unrelated", encoding="utf-8")
            result = audit_startup(folder)
            self.assertTrue(result["clean"])
            self.assertEqual(result["legacy_entries"], [])

    def test_old_path_or_name_is_flagged_in_run_values(self):
        self.assertTrue(is_legacy_value("Codex Status Pet", "pythonw.exe old.py"))
        self.assertTrue(is_legacy_value("Other", r"C:\Users\tangz\.agents\plugins\plugins\codex-windows-status-pet\scripts\codex_status_pet.py"))
        self.assertFalse(is_legacy_value("Ollama", "ollama.exe"))
