import gc
import itertools
import json
import runpy
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))


class DummyServer:
    def __init__(self, _queue):
        self.proc = None

    def stop(self):
        pass


class DummyTray:
    def __init__(self, _actions):
        pass

    def stop(self):
        pass


APPROVED_ROWS = {
    "activity": "Codex 输出中",
    "progress": "活动对话 1 个",
    "primary_5h": "5h 10% / 17:23",
    "weekly": "周 86% / 12:23 7/17",
    "reset_credit": "重置 5 次 / 18:40 7/12",
}


class ContentFitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(
            str(Path(__file__).parents[1] / "scripts" / "codex_status_pet.py")
        )
        cls.module["AppServer"] = DummyServer
        cls.module["TrayIcon3"] = DummyTray

    def new_app(self, scale):
        app = self.module["Pet"]()
        app.apply_settings(
            {
                **app.settings,
                "window_scale_percent": scale,
                "x": 100,
                "y": 100,
                "compact": False,
                "show_primary_5h": True,
                "show_weekly": True,
                "show_reset_credit": True,
            }
        )
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

    def test_supported_scales_allocate_every_requested_row(self):
        for scale in range(80, 201, 5):
            geometry = (
                round(330 * (scale / 100)),
                round(138 * (scale / 100)),
            )
            with self.subTest(scale=scale):
                app = self.new_app(scale)
                try:
                    app.text.configure_rows(rows=APPROVED_ROWS)
                    app.update()
                    self.assertEqual((app.winfo_width(), app.winfo_height()), geometry)
                    self.assertLessEqual(app.winfo_reqheight(), app.winfo_height())
                    self.assertLessEqual(
                        app.text.winfo_reqheight(), app.text.winfo_height()
                    )
                    for row_id, label in app.text.labels.items():
                        self.assertGreater(label.winfo_height(), 0, row_id)
                        self.assertLessEqual(
                            label.winfo_reqheight(), label.winfo_height(), row_id
                        )
                        self.assertLessEqual(
                            label.winfo_y() + label.winfo_height(),
                            app.text.winfo_height(),
                            row_id,
                        )
                    self.assertEqual(len(app.battery.cells), 10)
                    self.assertTrue(all(
                        cell.winfo_ismapped()
                        and cell.winfo_x() >= 0
                        and cell.winfo_y() >= 0
                        and cell.winfo_x() + cell.winfo_width() <= app.winfo_width()
                        and cell.winfo_y() + cell.winfo_height() <= app.winfo_height()
                        for cell in app.battery.cells
                    ))
                    reset = app.text.labels["reset_credit"]
                    self.assertLessEqual(reset.winfo_reqwidth(), reset.winfo_width())
                    self.assertLessEqual(
                        reset.winfo_x() + reset.winfo_width(), app.text.winfo_width()
                    )
                finally:
                    self.destroy_app(app)

    def test_all_visibility_combinations_fit_each_supported_scale(self):
        optional_ids = ("primary_5h", "weekly", "reset_credit")
        for scale in range(80, 201, 5):
            app = self.new_app(scale)
            try:
                for flags in itertools.product((False, True), repeat=3):
                    with self.subTest(scale=scale, flags=flags):
                        settings = dict(zip(
                            ("show_primary_5h", "show_weekly", "show_reset_credit"),
                            flags,
                        ))
                        metrics_before = app.window_metrics
                        app.apply_settings({**app.settings, **settings})
                        app.text.configure_rows(rows=APPROVED_ROWS)
                        app.update_idletasks()
                        visible_ids = tuple(
                            row_id
                            for row_id, label in app.text.labels.items()
                            if label.winfo_ismapped()
                        )
                        expected_ids = ("activity", "progress") + tuple(
                            row_id
                            for row_id, enabled in zip(optional_ids, flags)
                            if enabled
                        )
                        centers = tuple(
                            2 * app.text.labels[row_id].winfo_y()
                            + app.text.labels[row_id].winfo_height()
                            for row_id in visible_ids
                        )
                        self.assertEqual(visible_ids, expected_ids)
                        self.assertEqual(app.window_metrics, metrics_before)
                        self.assertLessEqual(
                            app.text.winfo_reqheight(), app.text.winfo_height()
                        )
                        self.assertTrue(all(
                            label.winfo_y() + label.winfo_height()
                            <= app.text.winfo_height()
                            for label in app.text.labels.values()
                            if label.winfo_ismapped()
                        ))
                        gaps = tuple(
                            right - left
                            for left, right in zip(centers, centers[1:])
                        )
                        self.assertLessEqual(max(gaps, default=0) - min(gaps, default=0), 2)
                        self.assertEqual(len(app.battery.cells), 10)
                        self.assertTrue(all(cell.winfo_ismapped() for cell in app.battery.cells))
            finally:
                self.destroy_app(app)

    def test_both_battery_sources_remain_independent_of_visibility_at_all_scales(self):
        optional_ids = ("primary_5h", "weekly", "reset_credit")
        sources = (
            ("primary_5h", "#a3e635", "#374151"),
            ("weekly", "#facc15", "#374151"),
        )
        for scale in range(80, 201, 5):
            app = self.new_app(scale)
            try:
                app.latest_quota = {
                    "rateLimits": {
                        "primary": {"usedPercent": 20},
                        "secondary": {"usedPercent": 45},
                    }
                }
                for source, last_lit, first_unlit in sources:
                    for flags in itertools.product((False, True), repeat=3):
                        with self.subTest(scale=scale, source=source, flags=flags):
                            settings = dict(zip(
                                ("show_primary_5h", "show_weekly", "show_reset_credit"),
                                flags,
                            ))
                            app.apply_settings({
                                **app.settings,
                                **settings,
                                "battery_quota_source": source,
                            })
                            app.render_status()
                            app.update_idletasks()
                            visible_ids = tuple(
                                row_id
                                for row_id, label in app.text.labels.items()
                                if label.winfo_ismapped()
                            )
                            expected_ids = ("activity", "progress") + tuple(
                                row_id
                                for row_id, enabled in zip(optional_ids, flags)
                                if enabled
                            )
                            self.assertEqual(visible_ids, expected_ids)
                            if source == "primary_5h":
                                self.assertEqual(app.battery.cells[7].cget("bg"), last_lit)
                                self.assertEqual(app.battery.cells[8].cget("bg"), first_unlit)
                            else:
                                self.assertEqual(app.battery.cells[5].cget("bg"), last_lit)
                                self.assertEqual(app.battery.cells[6].cget("bg"), first_unlit)
                            self.assertLessEqual(
                                app.text.winfo_reqheight(), app.text.winfo_height()
                            )
            finally:
                self.destroy_app(app)

    def test_supported_scales_keep_all_ten_compact_cells_inside_root(self):
        for scale in range(80, 201, 5):
            with self.subTest(scale=scale):
                app = self.new_app(scale)
                try:
                    app.set_compact(True)
                    app.update_idletasks()
                    app.update()
                    self.assertFalse(app.text.winfo_ismapped())
                    self.assertEqual(len(app.battery.cells), 10)
                    self.assertTrue(all(
                        cell.winfo_ismapped()
                        and cell.winfo_x() >= 0
                        and cell.winfo_y() >= 0
                        and cell.winfo_x() + cell.winfo_width() <= app.winfo_width()
                        and cell.winfo_y() + cell.winfo_height() <= app.winfo_height()
                        for cell in app.battery.cells
                    ))
                finally:
                    self.destroy_app(app)

    def test_production_dpi_startup_fits_every_supported_scale(self):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("dpi_content_probe.py"))],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, result)
        self.assertTrue(result["all_fit"])
        self.assertEqual(len(result["rows"]), 25)


if __name__ == "__main__":
    unittest.main()
