"""Fast, branch-local regression coverage for the Signal HUD redesign."""

import gc
import json
import runpy
import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


def widgets(root):
    for child in root.winfo_children():
        yield child
        yield from widgets(child)


class UiRedesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
        cls.module["AppServer"] = DummyServer
        cls.module["TrayIcon3"] = DummyTray

    def new_app(self):
        app = self.module["Pet"]()
        for callback in app.tk.call("after", "info"):
            app.after_cancel(callback)
        return app

    @staticmethod
    def destroy_app(app):
        app.application_controller.shutdown()
        for callback in app.tk.call("after", "info"):
            try:
                app.after_cancel(callback)
            except Exception:
                pass
        app.topmost_var = None
        app.locked_var = None
        app.destroy()
        gc.collect()

    def test_signal_hud_theme_is_stable_and_accessible(self):
        from ui.theme import COLORS, FONT_FAMILY

        self.assertEqual(FONT_FAMILY, "Segoe UI")
        self.assertEqual(COLORS["background"], "#0b1220")
        self.assertEqual(COLORS["text"], "#e5e7eb")
        self.assertEqual(COLORS["accent"], "#22d3ee")
        self.assertEqual(COLORS["success"], "#4ade80")

    def test_main_window_uses_hud_surface_without_changing_five_rows(self):
        app = self.new_app()
        try:
            self.assertEqual(app.cget("highlightbackground"), "#26354d")
            self.assertEqual(tuple(app.text.labels), ("activity", "progress", "primary_5h", "weekly", "reset_credit"))
            self.assertEqual(len(app.battery.cells), 10)
        finally:
            self.destroy_app(app)

    def test_settings_surface_has_navigation_preview_and_transactional_apply(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            path = home / ".codex" / "codex-windows-status-pet.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(CONFIG), encoding="utf-8")
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                app = self.new_app()
                app.show_settings()
                app.update_idletasks()
                texts = {
                    str(widget.cget("text"))
                    for widget in widgets(app.settings_dialog)
                    if "text" in widget.keys()
                }
                self.assertTrue({"General", "Appearance", "Quota display", "Behavior", "Advanced"} <= texts)
                self.assertIn("Live preview", texts)
                self.assertIn("Row visibility", texts)
                opening_topmost = app.settings["topmost"]
                checks = [widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Checkbutton)]
                checks[0].invoke()
                apply_button = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Button) and widget.cget("text") == "Apply")
                apply_button.invoke()
                self.assertNotEqual(app.settings["topmost"], opening_topmost)
            finally:
                if app is not None:
                    self.destroy_app(app)
                Path.home = original_home

    def test_context_menu_uses_hud_surface_and_keeps_actions(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.menu(type("Event", (), {"x_root": 4200, "y_root": 200})())
            popup = app.context_menu
            self.assertEqual(popup.cget("bg"), "#26354d")
            labels = [
                str(widget.cget("text"))
                for widget in widgets(popup)
                if isinstance(widget, (tk.Button, tk.Checkbutton))
            ]
            self.assertEqual(labels, ["Settings", "Always on top", "Lock position", "Compact", "Hide window", "Exit"])
        finally:
            if app.context_menu is not None and app.context_menu.winfo_exists():
                app.context_menu.destroy()
            self.destroy_app(app)


if __name__ == "__main__":
    unittest.main()
