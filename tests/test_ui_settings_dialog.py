import gc
import json
import runpy
import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


def _widgets(root):
    for child in root.winfo_children():
        yield child
        yield from _widgets(child)


class SettingsDialogTests(unittest.TestCase):
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
                    if isinstance(widget, tk.Button) and widget.cget("text") == "应用"
                ).invoke()
                self.assertEqual(app.settings["battery_quota_source"], "primary_5h")
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "关闭"
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
                    and widget.cget("text") == "显示周额度"
                )
                weekly_toggle.invoke()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "保存"
                ).invoke()
                self.assertFalse(app.settings["show_weekly"])
                self.assertFalse(app.load_settings()["show_weekly"])
                app.show_settings()
                app.update()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "恢复默认值"
                ).invoke()
                next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "应用"
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
                        and widget.cget("text") == "显示周额度"
                    ),
                    None,
                )
                self.assertIsNotNone(weekly_toggle)
                weekly_toggle.invoke()
                apply_button = next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "应用"
                )
                apply_button.invoke()
                app.update_idletasks()
                self.assertFalse(app.text.labels["weekly"].winfo_ismapped())
                close_button = next(
                    widget
                    for widget in _widgets(app.settings_dialog)
                    if isinstance(widget, tk.Button) and widget.cget("text") == "关闭"
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
