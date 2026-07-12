"""Regression tests for one long-lived Pet across runtime geometry transitions."""

from __future__ import annotations

import gc
import ctypes
import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.runtime_geometry_transition_probe import (
    CONFIG,
    DummyServer,
    DummyTray,
    ROWS,
    ROOT,
    capture,
)
from scripts.api.window_scale_api import derive_window_metrics


class RuntimeGeometryTransitionTests(unittest.TestCase):
    def test_toggle_preserves_cold_start_fit(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config_path = home / ".codex" / "codex-windows-status-pet.json"
            config_path.parent.mkdir(parents=True)
            config_path.write_text(json.dumps(CONFIG), encoding="utf-8")
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            dpi_patcher = None
            try:
                module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
                module["AppServer"] = DummyServer
                module["TrayIcon3"] = DummyTray
                main_window = sys.modules[module["Pet"].__mro__[1].__module__]
                def mixed_dpi_window(hwnd):
                    rect = (ctypes.c_long * 4)()
                    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    return 96 if rect[0] >= 2560 else 120

                dpi_patcher = mock.patch.object(
                    main_window, "dpi_for_window", side_effect=mixed_dpi_window
                )
                dpi_patcher.start()
                app = module["Pet"]()
                app.text.configure_rows(rows=ROWS)
                app.update_idletasks()
                app.update()
                cold = capture(app, "cold_start", "after_update")

                app.locked_var.set(not app.locked_var.get())
                app.toggle_locked()
                app.update_idletasks()
                app.update()
                toggled = capture(app, "toggle_locked_only", "after_update")

                self.assertTrue(cold["fits"])
                self.assertEqual(toggled["logical_scale"], cold["logical_scale"])
                self.assertEqual(toggled["dpi"], cold["dpi"])
                self.assertEqual(toggled["root_actual"], cold["root_actual"])
                self.assertEqual(len(toggled["labels"]), 5)
                self.assertTrue(toggled["fits"])
                self.assertLessEqual(
                    toggled["final_row_bottom"], toggled["visible_root_bottom"]
                )

                app.apply_settings(
                    {
                        **app.settings,
                        "x": 30,
                        "y": 120,
                        "window_scale_percent": 100,
                    }
                )
                app.update_idletasks()
                app.update()
                self.assertEqual(app.window_dpi, 120)
                self.assertEqual(
                    (app.window_metrics.width, app.window_metrics.height),
                    (412, 172),
                )

                for x, y, dpi in ((30, 120, 120), (4151, 1248, 96)):
                    for scale in range(80, 201, 5):
                        app.apply_settings(
                            {
                                **app.settings,
                                "x": x,
                                "y": y,
                                "window_scale_percent": scale,
                            }
                        )
                        app.update_idletasks()
                        app.update()
                        snapshot = capture(
                            app, f"dpi_{dpi}_scale_{scale}", "after_update"
                        )
                        expected = derive_window_metrics(scale, dpi=dpi)
                        self.assertEqual(app.window_dpi, dpi)
                        self.assertEqual(
                            snapshot["root_actual"],
                            [expected.width, expected.height],
                        )
                        self.assertTrue(snapshot["fits"])
            finally:
                if app is not None:
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
                if dpi_patcher is not None:
                    dpi_patcher.stop()
                Path.home = original_home


if __name__ == "__main__":
    unittest.main()
