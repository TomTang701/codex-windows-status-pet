import gc
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
            {**app.settings, "window_scale_percent": scale, "x": 100, "y": 100}
        )
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
                    reset = app.text.labels["reset_credit"]
                    self.assertLessEqual(reset.winfo_reqwidth(), reset.winfo_width())
                    self.assertLessEqual(
                        reset.winfo_x() + reset.winfo_width(), app.text.winfo_width()
                    )
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
