"""Fast, branch-local regression coverage for the Signal HUD redesign."""

import gc
import json
import runpy
import tempfile
import tkinter as tk
import unittest
from unittest.mock import patch
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

    def test_expanded_window_uses_two_card_signal_hud_composition(self):
        app = self.new_app()
        try:
            self.assertEqual(app.hud_header.winfo_parent(), str(app))
            self.assertEqual(app.status_card.winfo_parent(), str(app))
            self.assertEqual(app.signal_card.winfo_parent(), str(app))
            self.assertEqual(app.text.winfo_parent(), str(app.status_card))
            self.assertEqual(app.battery.winfo_parent(), str(app.signal_card))
            self.assertTrue(any(str(widget.cget("text")) == "CODEX" for widget in widgets(app.hud_header)))
            signal_title = app.signal_title
            self.assertEqual(signal_title.cget("fg"), "#818cf8")
            app.apply_settings({**app.settings, "battery_quota_source": "primary_5h"})
            self.assertEqual(signal_title.cget("fg"), "#22d3ee")
            app.set_compact(True)
            app.update_idletasks()
            self.assertFalse(app.hud_header.winfo_ismapped())
            self.assertFalse(app.status_card.winfo_ismapped())
            self.assertTrue(app.signal_card.winfo_ismapped())
            self.assertFalse(app.signal_title.winfo_ismapped())
            self.assertTrue(all(cell.winfo_ismapped() for cell in app.battery.cells))
            app.set_compact(False)
            app.update_idletasks()
            self.assertTrue(app.signal_title.winfo_ismapped())
        finally:
            self.destroy_app(app)

    def test_hud_cursor_explains_drag_and_lock_state(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "locked": False})
            self.assertEqual(app.cget("cursor"), "fleur")
            self.assertEqual(app.text.labels["activity"].cget("cursor"), "fleur")
            app.apply_settings({**app.settings, "locked": True})
            self.assertEqual(app.cget("cursor"), "arrow")
            self.assertEqual(app.text.labels["activity"].cget("cursor"), "arrow")
        finally:
            self.destroy_app(app)

    def test_hud_border_communicates_live_status_without_changing_rows(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.latest_activity = {"active": 1, "detail": "Outputting", "progress": "Active conversations  1"}
            app.latest_quota = {"rateLimits": {"primary": {"usedPercent": 20}, "secondary": {}}, "rateLimitResetCredits": {}}
            app.quota_state.update(app.latest_quota)
            app.render_status()
            self.assertEqual(app.cget("highlightbackground"), "#4ade80")
            self.assertEqual(app.status_card.cget("highlightbackground"), "#4ade80")
            self.assertEqual(app.signal_card.cget("highlightbackground"), "#4ade80")
            self.assertEqual(app.status_rail.cget("bg"), "#4ade80")
            app.quota_state.state = "unavailable"
            app.render_status()
            self.assertEqual(app.cget("highlightbackground"), "#f87171")
            self.assertEqual(app.status_card.cget("highlightbackground"), "#f87171")
            self.assertEqual(app.signal_card.cget("highlightbackground"), "#f87171")
            self.assertEqual(app.status_rail.cget("bg"), "#f87171")
            self.assertEqual(app.hud_status.cget("text"), "Quota unavailable")
            self.assertEqual(tuple(app.text.labels), ("activity", "progress", "primary_5h", "weekly", "reset_credit"))
        finally:
            self.destroy_app(app)

    def test_apply_settings_resets_all_hud_borders_to_neutral(self):
        app = self.new_app()
        try:
            app.quota_state.state = "unavailable"
            app.render_status()
            self.assertEqual(app.signal_card.cget("highlightbackground"), "#f87171")
            app.apply_settings({**app.settings, "language": "en"})
            self.assertEqual(app.cget("highlightbackground"), "#26354d")
            self.assertEqual(app.hud_header.cget("highlightbackground"), "#26354d")
            self.assertEqual(app.status_card.cget("highlightbackground"), "#26354d")
            self.assertEqual(app.signal_card.cget("highlightbackground"), "#26354d")
        finally:
            self.destroy_app(app)

    def test_signal_hud_labels_follow_runtime_language(self):
        from api.localization_api import translate

        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "zh-CN", "battery_quota_source": "weekly"})
            app.latest_activity = {"active": 1, "detail": "输出中", "progress": "活动对话 1 个"}
            app.render_status()
            self.assertEqual(app.hud_status.cget("text"), translate("zh-CN", "output"))
            self.assertEqual(app.signal_title.cget("text"), translate("zh-CN", "weekly"))
            app.apply_settings({**app.settings, "language": "en", "battery_quota_source": "primary_5h"})
            app.render_status()
            self.assertEqual(app.hud_status.cget("text"), translate("en", "output"))
            self.assertEqual(app.signal_title.cget("text"), translate("en", "five_hour"))
        finally:
            self.destroy_app(app)

    def test_signal_card_shows_remaining_percentage_in_expanded_mode(self):
        app = self.new_app()
        try:
            app.latest_quota = {
                "rateLimits": {"primary": {}, "secondary": {"usedPercent": 20}},
                "rateLimitResetCredits": {},
            }
            app.apply_settings({**app.settings, "language": "en", "battery_quota_source": "weekly"})
            app.render_status()
            self.assertEqual(app.signal_value.cget("text"), "80%")
            app.set_compact(True)
            app.update_idletasks()
            self.assertFalse(app.signal_value.winfo_ismapped())
            app.set_compact(False)
            app.update_idletasks()
            self.assertTrue(app.signal_value.winfo_ismapped())
        finally:
            self.destroy_app(app)

    def test_language_apply_updates_hud_status_without_waiting_for_refresh(self):
        from api.localization_api import translate

        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.latest_activity = {"active": 1}
            app.render_status()
            app.apply_settings({**app.settings, "language": "zh-CN"})
            self.assertEqual(app.hud_status.cget("text"), translate("zh-CN", "output"))
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

    def test_live_preview_matches_signal_hud_card_composition(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            preview_card = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Frame) and int(widget.cget("width")) == 190
            )
            preview_texts = {
                str(widget.cget("text"))
                for widget in widgets(preview_card)
                if isinstance(widget, tk.Label)
            }
            self.assertIn("CODEX", preview_texts)
            self.assertIn("SIGNAL", preview_texts)
            preview_live = next(widget for widget in widgets(preview_card) if isinstance(widget, tk.Label) and widget.cget("text") == "Outputting")
            self.assertEqual(preview_live.cget("fg"), "#4ade80")
            signal_panel = next(widget for widget in widgets(preview_card) if isinstance(widget, tk.Frame) and int(widget.cget("width")) == 42)
            self.assertGreaterEqual(signal_panel.winfo_width(), 42)
            signal_cells = [
                widget
                for widget in widgets(preview_card)
                if isinstance(widget, tk.Label) and int(widget.cget("width")) == 1
            ]
            self.assertEqual(len(signal_cells), 10)
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

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

    def test_color_draft_updates_live_preview_palette(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            font_button = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Button) and widget.cget("text") == "Font color..."
            )
            background_button = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Button) and widget.cget("text") == "Background color..."
            )
            preview_card = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Frame) and int(widget.cget("width")) == 190
            )
            preview_conversations = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and widget.cget("text") == "Active conversations  1"
            )
            self.assertEqual(font_button.cget("highlightbackground"), app.settings["font_color"])
            self.assertEqual(background_button.cget("highlightbackground"), app.settings["background_color"])
            with patch("ui.settings_dialog.colorchooser.askcolor", return_value=((18, 52, 86), "#123456")):
                font_button.invoke()
            self.assertEqual(preview_conversations.cget("fg"), "#123456")
            self.assertEqual(font_button.cget("highlightbackground"), "#123456")
            with patch("ui.settings_dialog.colorchooser.askcolor", return_value=((34, 51, 68), "#223344")):
                background_button.invoke()
            self.assertEqual(preview_card.cget("bg"), "#223344")
            self.assertEqual(background_button.cget("highlightbackground"), "#223344")
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_settings_form_has_quota_group_divider(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            dividers = [
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Frame)
                and widget.cget("bg") == "#26354d"
                and int(widget.cget("height")) == 1
            ]
            self.assertTrue(dividers)
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
            topmost = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Checkbutton) and widget.cget("text") == "Always on top"
            )
            opening_topmost = "topmost" in preview_meta.cget("text")
            topmost.invoke()
            app.update_idletasks()
            self.assertIn("normal" if opening_topmost else "topmost", preview_meta.cget("text"))
            lock_position = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Checkbutton) and widget.cget("text") == "Lock position"
            )
            lock_position.invoke()
            app.update_idletasks()
            lock_state = bool(int(app.getvar(lock_position.cget("variable"))))
            self.assertIn("locked" if lock_state else "drag enabled", preview_meta.cget("text"))
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
            self.assertIn("\u25cf  Codex \u8f93\u51fa\u4e2d", texts)
            self.assertIn("\u6d3b\u52a8\u5bf9\u8bdd 1 \u4e2a", texts)
            self.assertIn("\u6bcf\u5468\u989d\u5ea6   88%", texts)
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
            self.assertEqual(status.cget("text"), "Draft only · Apply to update")
            self.assertIn("Apply", status.cget("text"))
            apply_button = next(widget for widget in widgets(app.settings_dialog) if isinstance(widget, tk.Button) and widget.cget("text") == "Apply")
            apply_button.invoke()
            self.assertIn("Save", status.cget("text"))
            window_scale = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Scale) and float(widget.cget("to")) == 200.0
            )
            window_scale.set(150)
            app.update_idletasks()
            self.assertIn("Draft changed", status.cget("text"))
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_sidebar_navigation_highlights_section_and_focuses_target_control(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            appearance = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Button) and widget.cget("text") == "Appearance"
            )
            general = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Button) and widget.cget("text") == "General"
            )
            self.assertEqual(general.cget("bg"), "#172033")
            initial_target = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Scale) and float(widget.cget("to")) == 1.0
            )
            self.assertEqual(initial_target.cget("highlightthickness"), 1)
            appearance.invoke()
            self.assertEqual(appearance.cget("bg"), "#172033")
            self.assertEqual(general.cget("bg"), "#111827")
            target = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Scale) and float(widget.cget("to")) == 200.0
            )
            self.assertEqual(target.cget("highlightthickness"), 1)
            self.assertEqual(target.cget("highlightbackground"), "#22d3ee")
            self.assertEqual(initial_target.cget("highlightthickness"), 0)
            self.assertTrue(app.settings_dialog.focus_get())
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_settings_keyboard_shortcuts_apply_and_close(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            dialog = app.settings_dialog
            status = next(
                widget
                for widget in widgets(dialog)
                if isinstance(widget, tk.Label) and str(widget.cget("text")).startswith("Draft")
            )
            dialog.focus_force()
            dialog.event_generate("<Alt-a>")
            app.update_idletasks()
            self.assertIn("Save", status.cget("text"))
            dialog.event_generate("<Escape>")
            app.update_idletasks()
            self.assertFalse(dialog.winfo_exists())
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_settings_open_starts_keyboard_focus_in_general_section(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            app.update()
            focus = app.settings_dialog.focus_get()
            self.assertIsNotNone(focus)
            general = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Button) and widget.cget("text") == "General"
            )
            self.assertEqual(general.cget("bg"), "#172033")
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_live_preview_identifies_selected_quota_source(self):
        app = self.new_app()
        try:
            app.apply_settings({**app.settings, "language": "en"})
            app.show_settings()
            app.update_idletasks()
            source_scale = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Scale) and float(widget.cget("to")) == 1.0 and float(widget.cget("from")) == 0.0
            )
            source_scale.set(0)
            app.update_idletasks()
            source_label = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and str(widget.cget("text")).startswith("Source")
            )
            five_hour_label = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and widget.cget("text") == "5-hour"
            )
            weekly_label = next(
                widget
                for widget in widgets(app.settings_dialog)
                if isinstance(widget, tk.Label) and widget.cget("text") == "Weekly"
            )
            self.assertIn("5-hour", source_label.cget("text"))
            self.assertEqual(five_hour_label.cget("fg"), "#22d3ee")
            self.assertEqual(weekly_label.cget("fg"), "#94a3b8")
            source_scale.set(1)
            app.update_idletasks()
            self.assertEqual(five_hour_label.cget("fg"), "#94a3b8")
            self.assertEqual(weekly_label.cget("fg"), "#22d3ee")
            self.assertEqual(app.settings["battery_quota_source"], "weekly")
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
            menu_header = next(
                widget
                for widget in widgets(popup)
                if isinstance(widget, tk.Label) and widget.cget("text") == "CODEX"
            )
            self.assertEqual(menu_header.cget("fg"), "#22d3ee")
            first_item = next(
                widget
                for widget in widgets(popup)
                if isinstance(widget, (tk.Button, tk.Checkbutton))
                and widget.cget("text") == "Settings"
            )
            self.assertEqual(first_item.cget("highlightthickness"), 1)
            self.assertEqual(first_item.cget("highlightcolor"), "#22d3ee")
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
