"""Real mixed-DPI startup trace for target-monitor legal edge positions."""

from __future__ import annotations

import gc
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.api.display_api import monitor_snapshot
from scripts.api.runtime_api import enable_dpi_awareness
from scripts.api.window_recovery_api import rectangle_contained_in_work_area
from scripts.api.window_scale_api import derive_window_metrics
from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


def topology_from_monitors(monitors):
    """Return the physical topology required by the mixed-DPI host suite.

    These tests are physical-host evidence, not a synthetic monitor simulation.
    A host that lacks the measured topology is therefore not a failing product
    assertion and must report why it cannot supply that evidence.
    """
    primary = next((item for item in monitors if item["work"][0] == 0), None)
    secondary = next((item for item in monitors if item["work"][0] > 0), None)
    if primary is None or secondary is None or primary.get("dpi_x") != 120 or secondary.get("dpi_x") != 96:
        raise unittest.SkipTest(
            "required 125% primary / 100% right-side secondary topology unavailable"
        )
    return primary, secondary


class MixedDpiStartupPositionTests(unittest.TestCase):
    @staticmethod
    def destroy_app(app):
        if app is None:
            return
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

    def mixed_dpi_topology(self):
        enable_dpi_awareness()
        return topology_from_monitors(monitor_snapshot())

    def start_saved_position(self, saved, scale=85):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings_path = home / ".codex" / "codex-windows-status-pet.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(
                json.dumps(
                    {
                        **CONFIG,
                        "x": saved[0],
                        "y": saved[1],
                        "window_scale_percent": scale,
                        "font_size": 8,
                        "window_width": 280,
                        "window_height": 117,
                    }
                ),
                encoding="utf-8",
            )
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                app = module["Pet"]()
                app.update_idletasks()
                app.update()
                return (app.winfo_rootx(), app.winfo_rooty()), (app.winfo_width(), app.winfo_height())
            finally:
                self.destroy_app(app)
                Path.home = original_home

    def test_secondary_bottom_right_legal_at_target_dpi_survives_startup(self):
        primary, secondary = self.mixed_dpi_topology()
        scale = 85
        target_metrics = derive_window_metrics(scale, dpi=96)
        bootstrap_metrics = derive_window_metrics(scale, dpi=120)
        left, top, right, bottom = secondary["work"]
        saved = (right - target_metrics.width, bottom - target_metrics.height)
        self.assertTrue(
            rectangle_contained_in_work_area(
                *saved, target_metrics.width, target_metrics.height, secondary["work"]
            )
        )
        self.assertFalse(
            rectangle_contained_in_work_area(
                *saved, bootstrap_metrics.width, bootstrap_metrics.height, secondary["work"]
            )
        )

        trace = {
            "primary": primary,
            "secondary": secondary,
            "saved": list(saved),
            "target_metrics_96": [target_metrics.width, target_metrics.height],
            "bootstrap_metrics_120": [bootstrap_metrics.width, bootstrap_metrics.height],
            "dpi_calls": [],
            "safe_position": [],
            "recovery": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings_path = home / ".codex" / "codex-windows-status-pet.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(
                json.dumps(
                    {
                        **CONFIG,
                        "x": saved[0],
                        "y": saved[1],
                        "window_scale_percent": scale,
                        "font_size": 8,
                        "window_width": 280,
                        "window_height": 117,
                    }
                ),
                encoding="utf-8",
            )
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                main_window = module["_main_window"]
                original_dpi_for_window = main_window.dpi_for_window
                original_safe_position = module["Pet"].safe_position
                original_recover_position = main_window.recover_position

                def traced_dpi(hwnd):
                    dpi = original_dpi_for_window(hwnd)
                    trace["dpi_calls"].append({"hwnd": int(hwnd), "dpi": dpi})
                    return dpi

                def traced_recovery(x, y, width, height, observed_monitors, fallback):
                    output = original_recover_position(x, y, width, height, observed_monitors, fallback)
                    trace["recovery"].append(
                        {
                            "input": [x, y, width, height],
                            "contained": [
                                rectangle_contained_in_work_area(x, y, width, height, item["work"])
                                for item in observed_monitors
                            ],
                            "output": list(output),
                        }
                    )
                    return output

                def traced_safe_position(pet, x, y):
                    before = {
                        "input": [x, y],
                        "window_dpi": getattr(pet, "window_dpi", None),
                        "metrics": [pet.window_metrics.width, pet.window_metrics.height]
                        if hasattr(pet, "window_metrics")
                        else None,
                    }
                    output = original_safe_position(pet, x, y)
                    before["output"] = list(output)
                    trace["safe_position"].append(before)
                    return output

                main_window.dpi_for_window = traced_dpi
                main_window.recover_position = traced_recovery
                module["Pet"].safe_position = traced_safe_position
                try:
                    app = module["Pet"]()
                    app.update_idletasks()
                    app.update()
                    trace["final"] = {
                        "root": [app.winfo_rootx(), app.winfo_rooty()],
                        "window_dpi": app.window_dpi,
                        "metrics": [app.window_metrics.width, app.window_metrics.height],
                        "settings": [app.settings["x"], app.settings["y"]],
                        "persisted": json.loads(settings_path.read_text(encoding="utf-8")),
                    }
                finally:
                    main_window.dpi_for_window = original_dpi_for_window
                    main_window.recover_position = original_recover_position
                    module["Pet"].safe_position = original_safe_position
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

        artifact = ROOT / ".build" / "v055-mixed-dpi-startup-trace.json"
        artifact.parent.mkdir(exist_ok=True)
        artifact.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
        self.assertEqual(
            tuple(trace["final"]["root"]),
            saved,
            f"startup changed target-DPI legal saved position; trace={artifact}",
        )

    def test_secondary_legal_edge_and_interior_positions_survive_startup(self):
        _primary, secondary = self.mixed_dpi_topology()
        metrics = derive_window_metrics(85, dpi=secondary["dpi_x"])
        left, top, right, bottom = secondary["work"]
        positions = {
            "right": (right - metrics.width, top + 100),
            "bottom": (left + 100, bottom - metrics.height),
            "bottom_right": (right - metrics.width, bottom - metrics.height),
            "interior": (left + 100, top + 100),
        }
        for name, saved in positions.items():
            with self.subTest(position=name):
                root, size = self.start_saved_position(saved)
                self.assertEqual(root, saved)
                self.assertEqual(size, (metrics.width, metrics.height))

    def test_primary_edge_and_invalid_coordinate_keep_distinct_recovery_contracts(self):
        primary, secondary = self.mixed_dpi_topology()
        primary_metrics = derive_window_metrics(85, dpi=primary["dpi_x"])
        left, top, right, bottom = primary["work"]
        legal_primary = (right - primary_metrics.width, bottom - primary_metrics.height)
        root, size = self.start_saved_position(legal_primary)
        self.assertEqual(root, legal_primary)
        self.assertEqual(size, (primary_metrics.width, primary_metrics.height))

        invalid = (secondary["work"][2] + 500, secondary["work"][3] + 500)
        root, size = self.start_saved_position(invalid)
        self.assertNotEqual(root, invalid)
        self.assertTrue(
            any(
                rectangle_contained_in_work_area(*root, *size, monitor["work"])
                for monitor in (primary, secondary)
            )
        )

    def test_secondary_edge_drag_exit_restart_preserves_exact_position(self):
        _primary, secondary = self.mixed_dpi_topology()
        metrics = derive_window_metrics(85, dpi=secondary["dpi_x"])
        left, top, right, bottom = secondary["work"]
        initial = (left + 100, top + 100)
        target = (right - metrics.width, bottom - metrics.height)
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings_path = home / ".codex" / "codex-windows-status-pet.json"
            settings_path.parent.mkdir(parents=True)
            settings_path.write_text(
                json.dumps({**CONFIG, "x": initial[0], "y": initial[1], "window_scale_percent": 85, "locked": True}),
                encoding="utf-8",
            )
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app_a = app_b = None
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                pet_type = module["Pet"]
                app_a = pet_type()
                app_a.update()
                app_a.locked_var.set(False)
                app_a.toggle_locked()
                app_a.start_drag(SimpleNamespace(x_root=app_a.winfo_rootx() + 12, y_root=app_a.winfo_rooty() + 12))
                app_a.drag(SimpleNamespace(x_root=target[0] + 12, y_root=target[1] + 12))
                app_a.update_idletasks()
                app_a.update()
                app_a.finish_drag(SimpleNamespace())
                self.assertEqual((app_a.winfo_rootx(), app_a.winfo_rooty()), target)
                self.assertEqual((json.loads(settings_path.read_text(encoding="utf-8"))["x"], json.loads(settings_path.read_text(encoding="utf-8"))["y"]), target)
                for callback in app_a.tk.call("after", "info"):
                    app_a.after_cancel(callback)
                app_a.close()
                app_a = None

                app_b = pet_type()
                app_b.update_idletasks()
                app_b.update()
                self.assertEqual((app_b.winfo_rootx(), app_b.winfo_rooty()), target)
            finally:
                self.destroy_app(app_a)
                self.destroy_app(app_b)
                Path.home = original_home


if __name__ == "__main__":
    unittest.main()
