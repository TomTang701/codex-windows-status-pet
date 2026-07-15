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

    def test_settings_controls_use_dark_theme_and_primary_action(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            opacity = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Label) and widget.cget("text") == "Opacity")
            save = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Button) and widget.cget("text") == "Save")
            entries = [widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Entry) and widget.winfo_class() == "Entry"]
            self.assertEqual(opacity.cget("bg"), "#0b1220")
            self.assertEqual(save.cget("bg"), "#22d3ee")
            self.assertEqual(save.cget("fg"), "#0b1220")
            self.assertTrue(entries)
            self.assertTrue(all(entry.cget("bg") == "#111827" for entry in entries))
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_activity_row_has_primary_visual_weight(self):
        app = self.new_app()
        try:
            import tkinter.font as tkfont

            activity_font = tkfont.Font(root=app, font=app.text.labels["activity"].cget("font"))
            progress_font = tkfont.Font(root=app, font=app.text.labels["progress"].cget("font"))
            self.assertEqual(activity_font.cget("weight"), "bold")
            self.assertEqual(progress_font.cget("weight"), "normal")
        finally:
            self.destroy_app(app)

    def test_live_preview_tracks_visibility_and_window_scale_draft(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            opening_scale = app.settings["window_scale_percent"]
            weekly_preview = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and widget.cget("text") == "Weekly quota   88%"
            )
            self.assertEqual(weekly_preview.winfo_manager(), "pack")
            weekly_toggle = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Checkbutton) and widget.cget("text") == "Show weekly quota"
            )
            weekly_toggle.invoke()
            app.update_idletasks()
            self.assertEqual(weekly_preview.winfo_manager(), "")
            scale = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Scale) and float(widget.cget("to")) == 200.0
            )
            scale.set(150)
            app.update_idletasks()
            preview_meta = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and str(widget.cget("text")).startswith("Preview")
            )
            self.assertIn("150%", preview_meta.cget("text"))
            self.assertEqual(app.settings["window_scale_percent"], opening_scale)
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_language_switch_updates_navigation_preview_titles_and_combobox_style(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            language_combo = next(widget for widget in widgets(app.settings_dialog) if widget.winfo_class() == "TCombobox")
            self.assertEqual(language_combo.cget("style"), "HUD.TCombobox")
            language_combo.set("Simplified Chinese")
            apply_button = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Button) and widget.cget("text") == "Apply")
            apply_button.invoke()
            texts = {
                str(widget.cget("text"))
                for widget in widgets(app.settings_dialog)
                if "text" in widget.keys()
            }
            self.assertIn("\u901a\u7528", texts)
            self.assertIn("\u9884\u89c8", texts)
            self.assertIn("\u884c\u53ef\u89c1\u6027", texts)
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_settings_status_explains_draft_apply_and_save_lifecycle(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            status = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and str(widget.cget("text")).startswith("Draft")
            )
            self.assertIn("Apply", status.cget("text"))
            apply_button = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Button) and widget.cget("text") == "Apply")
            apply_button.invoke()
            self.assertIn("Save", status.cget("text"))
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_context_menu_uses_hud_surface_and_keeps_actions(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.menu(type("Event", (), {"x_root": 4200, "y_root": 200})())
            popup = app.context_menu
            self.assertEqual(popup.cget("bg"), "#26354d")
            checkbuttons = [widget for widget in widgets(popup) if isinstance(widget, tk.Checkbutton)]
            self.assertTrue(checkbuttons)
            self.assertTrue(all(widget.cget("selectcolor") == "#172033" for widget in checkbuttons))
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
