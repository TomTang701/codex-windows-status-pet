import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.settings_session_api import SettingsSession


class SettingsSessionTests(unittest.TestCase):
    def setUp(self):
        self.original = {"x": 10, "topmost": False}
        self.session = SettingsSession(self.original)

    def test_apply_changes_runtime_but_not_persisted(self):
        self.session.draft_settings["x"] = 20
        self.assertEqual(self.session.apply()["x"], 20)
        self.assertEqual(self.session.persisted_settings["x"], 10)

    def test_close_discards_applied_preview(self):
        self.session.draft_settings["x"] = 20
        self.session.apply()
        self.assertEqual(self.session.close()["x"], 10)

    def test_save_updates_persisted_and_close_keeps_saved_value(self):
        self.session.draft_settings["x"] = 20
        self.assertEqual(self.session.save()["x"], 20)
        self.assertEqual(self.session.close()["x"], 20)

    def test_restore_defaults_only_changes_draft(self):
        self.session.restore_defaults({"x": 99, "topmost": True})
        self.assertEqual(self.session.draft_settings["x"], 99)
        self.assertEqual(self.session.persisted_settings["x"], 10)
