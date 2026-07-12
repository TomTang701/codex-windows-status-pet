import gc
import json
import runpy
import tempfile
import tkinter as tk
import unittest
from unittest.mock import patch
from pathlib import Path

from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


def _widgets(root):
    for child in root.winfo_children():
        yield child
        yield from _widgets(child)


class SettingsDialogTests(unittest.TestCase):
    def test_invalid_settings_warning_uses_current_dialog_language(self):
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
                app.update()
                entries = [
                    widget for widget in _widgets(app.settings_dialog)
                    if widget.winfo_class() == "Entry"
                ]
                entries[-1].delete(0, "end")
                self.assertEqual(entries[-1].get(), "")
                with patch("ui.settings_dialog.messagebox.showerror") as showerror:
                    next(
                        widget for widget in _widgets(app.settings_dialog)
                        if isinstance(widget, tk.Button) and widget.cget("text") == "Apply"
                    ).invoke()
                self.assertEqual(showerror.call_args.args[0], "Invalid settings")
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

    def test_language_dropdown_is_readonly_and_apply_preview_close_restores(self):
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
                app.update()
                language = next(
                    widget for widget in _widgets(app.settings_dialog)
                    if widget.winfo_class() == "TCombobox"
                )
                self.assertEqual(str(language.cget("state")), "readonly")
                self.assertEqual(language.get(), "English")
                language.set("Simplified Chinese")
                next(
                    widget for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Apply"
                ).invoke()
                self.assertEqual(app.settings["language"], "zh-CN")
                self.assertEqual(app.settings_dialog.title(), "Codex 宠物设置")
                self.assertEqual(language.get(), "简体中文")
                self.assertTrue(
                    any(
                        isinstance(widget, tk.Button) and widget.cget("text") == "应用"
                        for widget in _widgets(app.settings_dialog)
                    )
                )
                next(
                    widget for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "关闭"
                ).invoke()
                self.assertEqual(app.settings["language"], "en")
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

    def test_source_scale_apply_close_and_defaults_are_transactional(self):
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
                app.latest_quota = {
                    "rateLimits": {
                        "primary": {"usedPercent": 20},
                        "secondary": {"usedPercent": 45},
                    }
                }
                app.show_settings()
                app.update()
                source_scale = next(
                    (
                        widget
                        for widget in _widgets(app.settings_dialog)
                        if isinstance(widget, tk.Scale)
                        and float(widget.cget("from")) == 0
                        and float(widget.cget("to")) == 1
                    ),
                    None,
                )
                self.assertIsNotNone(source_scale)
                source_scale.set(0)
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Apply"
                ).invoke()
                self.assertEqual(app.settings["battery_quota_source"], "primary_5h")
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Close"
                ).invoke()
                self.assertEqual(app.settings["battery_quota_source"], "weekly")
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

    def test_save_persists_visibility_and_restore_defaults_reenables_every_row(self):
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
                app.update()
                weekly_toggle = next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Checkbutton)
                    and widget.cget("text") == "Show weekly quota"
                )
                weekly_toggle.invoke()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Save"
                ).invoke()
                self.assertFalse(app.settings["show_weekly"])
                self.assertFalse(app.load_settings()["show_weekly"])
                app.show_settings()
                app.update()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Restore Defaults"
                ).invoke()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Apply"
                ).invoke()
                app.update_idletasks()
                self.assertTrue(app.settings["show_primary_5h"])
                self.assertTrue(app.settings["show_weekly"])
                self.assertTrue(app.settings["show_reset_credit"])
                self.assertTrue(all(
                    label.winfo_ismapped() for label in app.text.labels.values()
                ))
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

    def test_apply_weekly_visibility_then_close_restores_opening_layout(self):
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
                app.update()
                weekly_toggle = next(
                    (
                        widget
                        for widget in _widgets(app.settings_dialog)
                        if isinstance(widget, tk.Checkbutton)
                        and widget.cget("text") == "Show weekly quota"
                    ),
                    None,
                )
                self.assertIsNotNone(weekly_toggle)
                weekly_toggle.invoke()
                apply_button = next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Apply"
                )
                apply_button.invoke()
                app.update_idletasks()
                self.assertFalse(app.text.labels["weekly"].winfo_ismapped())
                close_button = next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "Close"
                )
                close_button.invoke()
                app.update_idletasks()
                self.assertTrue(app.text.labels["weekly"].winfo_ismapped())
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
