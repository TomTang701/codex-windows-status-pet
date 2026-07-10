import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from ui.main_window import Pet


class ConfigurationWriteGuardTests(unittest.TestCase):
    def _read_only_app(self, path):
        return SimpleNamespace(
            config_writable=False,
            config_schema_status="unsupported_future",
            settings_path=path,
            settings={"schema_version": 1, "x": 30, "y": 120, "locked": False},
        )

    def test_future_schema_save_guard_preserves_original_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "future": "keep"})
            path.write_text(original, encoding="utf-8")
            app = self._read_only_app(path)
            with patch("ui.main_window.save_settings_atomic") as save:
                self.assertFalse(Pet.save_settings(app))
            save.assert_not_called()
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_hide_and_drag_autosaves_route_through_guard(self):
        app = SimpleNamespace(
            hidden=False,
            hidden_position=(30, 120),
            settings={"x": 30, "y": 120, "locked": False},
            save_settings=lambda: False,
            attributes=lambda *_args: None,
        )
        Pet.hide_window(app)
        Pet.finish_drag(app, None)
        self.assertTrue(app.hidden)

    def test_explicit_reset_reenables_current_schema_writes(self):
        app = self._read_only_app(Path("unused"))
        Pet.authorize_configuration_reset(app)
        self.assertTrue(app.config_writable)
        self.assertEqual(app.config_schema_status, "current")

