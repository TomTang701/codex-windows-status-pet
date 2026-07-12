"""Production-equivalent drag -> tray Exit -> restart position trace."""

from __future__ import annotations

import gc
import json
import runpy
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.api.display_api import monitor_snapshot, work_area_for_point
from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


class PositionPersistenceTests(unittest.TestCase):
    def test_drag_tray_exit_restart_preserves_stable_root_position(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings_path = home / ".codex" / "codex-windows-status-pet.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(
                json.dumps(
                    {
                        **CONFIG,
                        "window_scale_percent": 90,
                        "font_size": 9,
                        "window_width": 297,
                        "window_height": 124,
                        "x": 4183,
                        "y": 1262,
                        "locked": True,
                    }
                ),
                encoding="utf-8",
            )
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app_a = None
            app_b = None
            trace = []
            safe_calls = []
            raw_loads = []
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                pet_type = module["Pet"]
                original_safe_position = pet_type.safe_position
                original_load_settings = pet_type.load_settings

                def traced_safe_position(app, x, y):
                    output = original_safe_position(app, x, y)
                    safe_calls.append({"input": [x, y], "output": list(output)})
                    return output

                def traced_load_settings(app):
                    settings = original_load_settings(app)
                    raw_loads.append(dict(settings))
                    return settings

                pet_type.safe_position = traced_safe_position
                pet_type.load_settings = traced_load_settings
                try:
                    app_a = pet_type()
                    app_a.update_idletasks()
                    app_a.update()
                    self.record(trace, "Pet A initial", app_a, settings_path)

                    app_a.locked_var.set(False)
                    app_a.toggle_locked()
                    self.record(trace, "after normal unlock", app_a, settings_path)
                    self.assertFalse(app_a.settings["locked"])

                    initial_x, initial_y = app_a.winfo_rootx(), app_a.winfo_rooty()
                    left, top, right, bottom = work_area_for_point(initial_x, initial_y)
                    target_x = min(max(initial_x + 80, left + 40), right - app_a.winfo_width() - 40)
                    target_y = min(max(initial_y - 80, top + 40), bottom - app_a.winfo_height() - 40)
                    self.assertNotEqual((target_x, target_y), (initial_x, initial_y))

                    app_a.start_drag(SimpleNamespace(x_root=initial_x + 12, y_root=initial_y + 12))
                    app_a.drag(SimpleNamespace(x_root=target_x + 12, y_root=target_y + 12))
                    self.settle_scheduled_callbacks(app_a)
                    expected = (app_a.winfo_rootx(), app_a.winfo_rooty())
                    self.assertNotEqual(expected, (initial_x, initial_y))
                    self.record(trace, "after drag actual root", app_a, settings_path)
                    self.record(trace, "after drag settings", app_a, settings_path)

                    app_a.finish_drag(SimpleNamespace())
                    self.record(trace, "after finish_drag JSON", app_a, settings_path)
                    self.assertEqual(self.persisted_position(settings_path), expected)

                    self.record(trace, "before close settings", app_a, settings_path)
                    self.cancel_scheduled_callbacks(app_a)
                    app_a.tray_actions.put("exit")
                    app_a.process_tray_actions()
                    self.assertTrue(app_a.closing)
                    self.assertEqual(self.persisted_position(settings_path), expected)
                    trace.append({"boundary": "after close JSON", "persisted_json": self.persisted_position(settings_path)})
                    app_a = None

                    safe_calls.clear()
                    app_b = pet_type()
                    app_b.update_idletasks()
                    app_b.update()
                    self.assertEqual((raw_loads[-1]["x"], raw_loads[-1]["y"]), expected)
                    trace.append({"boundary": "Pet B raw loaded settings", "raw_loaded": [raw_loads[-1]["x"], raw_loads[-1]["y"]]})
                    trace.append({"boundary": "Pet B safe_position", "safe_position": safe_calls[-1]})
                    self.record(trace, "Pet B final root", app_b, settings_path)

                    artifact = ROOT / ".build" / "v054-position-persistence-trace.json"
                    artifact.parent.mkdir(exist_ok=True)
                    artifact.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
                    self.assertEqual((app_b.winfo_rootx(), app_b.winfo_rooty()), expected)
                finally:
                    pet_type.safe_position = original_safe_position
                    pet_type.load_settings = original_load_settings
            finally:
                self.destroy_if_open(app_a)
                self.destroy_if_open(app_b)
                Path.home = original_home

    @staticmethod
    def persisted_position(path):
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload["x"], payload["y"]

    @staticmethod
    def settle_scheduled_callbacks(app):
        deadline = time.monotonic() + 2.3
        while time.monotonic() < deadline:
            app.update_idletasks()
            app.update()
            time.sleep(0.02)

    @staticmethod
    def record(trace, boundary, app, settings_path):
        monitor = next(
            (
                item
                for item in monitor_snapshot()
                if item["work"][0] <= app.winfo_rootx() < item["work"][2]
                and item["work"][1] <= app.winfo_rooty() < item["work"][3]
            ),
            None,
        )
        trace.append(
            {
                "boundary": boundary,
                "actual_root": [app.winfo_rootx(), app.winfo_rooty()],
                "settings": [app.settings["x"], app.settings["y"]],
                "persisted_json": PositionPersistenceTests.persisted_position(settings_path),
                "window_metrics": [app.window_metrics.width, app.window_metrics.height],
                "effective_dpi": app.window_dpi,
                "monitor_identity": monitor.get("name") if monitor else None,
                "monitor_work_area": monitor.get("work") if monitor else None,
            }
        )

    @staticmethod
    def destroy_if_open(app):
        if app is None:
            return
        try:
            app.application_controller.shutdown()
            for callback in app.tk.call("after", "info"):
                app.after_cancel(callback)
            app.topmost_var = None
            app.locked_var = None
            app.destroy()
            gc.collect()
        except Exception:
            pass

    @staticmethod
    def cancel_scheduled_callbacks(app):
        """Avoid executing stale test-root callbacks after the real close chain."""
        for callback in app.tk.call("after", "info"):
            app.after_cancel(callback)


if __name__ == "__main__":
    unittest.main()
