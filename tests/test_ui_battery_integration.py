"""Expanded-mode integration contract for the approved segmented battery."""

import gc
import json
import runpy
import tempfile
import unittest
from pathlib import Path

from scripts.api.status_snapshot_api import battery_presentation
from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


class BatteryIntegrationTests(unittest.TestCase):
    def test_compact_battery_uses_the_same_selected_primary_presentation(self):
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
                app.apply_settings({
                    **app.settings,
                    "battery_quota_source": "primary_5h",
                })
                app.render_status()
                app.set_compact(True)
                app.update_idletasks()
                self.assertTrue(all(cell.winfo_ismapped() for cell in app.battery.cells))
                self.assertEqual(app.battery.cells[7].cget("bg"), "#a3e635")
                self.assertEqual(app.battery.cells[8].cget("bg"), "#374151")
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

    def test_apply_source_change_updates_battery_without_changing_row_visibility(self):
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
                visible_ids = tuple(
                    row_id for row_id, label in app.text.labels.items()
                    if label.winfo_ismapped()
                )
                app.latest_quota = {
                    "rateLimits": {
                        "primary": {"usedPercent": 20},
                        "secondary": {"usedPercent": 45},
                    }
                }
                app.apply_settings({
                    **app.settings,
                    "battery_quota_source": "primary_5h",
                })
                app.render_status()
                self.assertEqual(app.battery.cells[7].cget("bg"), "#a3e635")
                self.assertEqual(
                    tuple(
                        row_id for row_id, label in app.text.labels.items()
                        if label.winfo_ismapped()
                    ),
                    visible_ids,
                )
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

    def test_apply_settings_forwards_row_visibility_without_changing_battery_metrics(self):
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
                before = app.window_metrics
                app.apply_settings({**app.settings, "show_weekly": False})
                app.update_idletasks()
                self.assertFalse(app.text.labels["weekly"].winfo_ismapped())
                self.assertEqual(app.window_metrics, before)
                self.assertEqual(len(app.battery.cells), 10)
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

    def test_compact_mode_shows_only_the_complete_ten_cell_battery(self):
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
                app.latest_quota = {"rateLimits": {"secondary": {"usedPercent": 22}}}
                app.render_status()
                app.set_compact(True)
                app.update_idletasks()
                app.update()
                self.assertFalse(app.text.winfo_ismapped())
                self.assertTrue(all(cell.winfo_ismapped() for cell in app.battery.cells))
                self.assertTrue(all(
                    cell.winfo_x() >= 0 and cell.winfo_y() >= 0
                    and cell.winfo_x() + cell.winfo_width() <= app.winfo_width()
                    and cell.winfo_y() + cell.winfo_height() <= app.winfo_height()
                    for cell in app.battery.cells
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

    def test_expanded_window_has_five_rows_and_interactive_battery_without_paw(self):
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
                app.latest_quota = {"rateLimits": {"secondary": {"usedPercent": 22}}}
                app.render_status()
                app.update_idletasks()
                app.update()

                self.assertFalse(hasattr(app, "face"))
                self.assertEqual(tuple(app.text.labels), ("activity", "progress", "primary_5h", "weekly", "reset_credit"))
                self.assertEqual(len(app.battery.cells), 10)
                self.assertEqual(app.battery.cells[0].cget("bg"), battery_presentation({"usedPercent": 22})["segments"][0]["color"])
                for widget in app.battery.event_widgets:
                    self.assertTrue(widget.bind("<Button-3>"))
                    self.assertTrue(widget.bind("<Enter>"))
                    self.assertTrue(widget.bind("<Button-1>"))
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
