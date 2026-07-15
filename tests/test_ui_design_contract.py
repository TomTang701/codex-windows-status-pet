import gc
import json
import runpy
import tkinter as tk
import tempfile
import unittest
from pathlib import Path

from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


def _widgets(root):
    for child in root.winfo_children():
        yield child
        yield from _widgets(child)


class UiDesignContractTests(unittest.TestCase):
    def test_signal_hud_theme_exposes_distinct_status_palette(self):
        from ui.theme import COLORS, FONT_FAMILY

        self.assertEqual(FONT_FAMILY, "Segoe UI")
        self.assertEqual(COLORS["background"], "#0b1220")
        self.assertEqual(COLORS["accent"], "#22d3ee")
        self.assertEqual(COLORS["success"], "#4ade80")
        self.assertEqual(COLORS["warning"], "#fbbf24")
        self.assertEqual(COLORS["danger"], "#f87171")

    def test_settings_dialog_exposes_grouped_navigation_and_live_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            path = home / ".codex" / "codex-windows-status-pet.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(CONFIG), encoding="utf-8")
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                app = module["Pet"]()
                app.show_settings()
                app.update_idletasks()
                texts = {
                    str(widget.cget("text"))
                    for widget in _widgets(app.settings_dialog)
                    if "text" in widget.keys()
                }
                self.assertTrue({"General", "Appearance", "Quota display", "Behavior", "Advanced"} <= texts)
                self.assertIn("Live preview", texts)
                self.assertIn("Row visibility", texts)
            finally:
                if app is not None:
                    app.application_controller.shutdown()
                    for callback in app.tk.call("after", "info"):
                        app.after_cancel(callback)
                    app.topmost_var = None
                    app.locked_var = None
                    app.destroy()
                    gc.collect()
                Path.home = original_home


if __name__ == "__main__":
    unittest.main()
