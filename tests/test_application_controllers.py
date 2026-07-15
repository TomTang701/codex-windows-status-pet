import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.application_controller_api import ApplicationController
from api.config_api import ConfigWriteProtectedError, DEFAULT_SETTINGS
from api.settings_persistence_controller_api import SettingsPersistenceController
from api.status_presentation_controller_api import StatusPresentationController
from api.status_rows_api import ROW_IDS
from api.window_lifecycle_controller_api import WindowLifecycleController


class ApplicationControllerTests(unittest.TestCase):
    def test_activity_and_quota_generations_are_independent(self):
        controller = ApplicationController(5)
        activity = controller.begin_activity()
        quota = controller.begin_quota()
        self.assertIsNotNone(activity)
        self.assertIsNotNone(quota)
        self.assertTrue(controller.is_current("activity", activity))
        self.assertTrue(controller.is_current("quota", quota))
        controller.finish("activity", activity)
        self.assertTrue(controller.is_current("quota", quota))
        controller.finish("quota", quota)

    def test_quota_is_single_flight_and_interval_is_bounded(self):
        controller = ApplicationController(99)
        generation = controller.begin_quota()
        self.assertIsNotNone(generation)
        self.assertIsNone(controller.begin_quota())
        self.assertEqual(controller.quota_delay_ms, 10000)
        controller.finish("quota", generation)
        self.assertIsNotNone(controller.begin_quota())

    def test_shutdown_prevents_new_generations(self):
        controller = ApplicationController(5)
        controller.shutdown()
        self.assertIsNone(controller.begin_activity())
        self.assertIsNone(controller.begin_quota())

    def test_lifecycle_close_is_idempotent(self):
        lifecycle = WindowLifecycleController()
        self.assertTrue(lifecycle.begin_close())
        self.assertFalse(lifecycle.begin_close())

    def test_presentation_controller_preserves_rows_without_auto_compact_behavior(self):
        controller = StatusPresentationController()
        snapshot = controller.render(
            {"active": 1, "detail": "输出中", "progress": "活动对话 1 个"},
            {"rateLimits": {}, "rateLimitResetCredits": {"availableCount": 5}},
            "ok", "#ffffff",
        )
        self.assertEqual(snapshot["rows"]["reset_credit"], "重置 5 次")
        self.assertFalse(hasattr(controller, "compact"))

    def test_presentation_controller_builds_approved_tray_error_rows(self):
        result = StatusPresentationController().render_tray_error()
        self.assertEqual(result["rows"]["activity"], "Codex")
        self.assertEqual(result["rows"]["progress"], "托盘图标异常")
        self.assertEqual(tuple(result["rows"]), ROW_IDS)
        self.assertEqual(result["color"], "#fca5a5")

    def test_presentation_controller_forwards_runtime_language_only_to_visible_text(self):
        snapshot = StatusPresentationController().render(
            {"active": 0, "detail": "Idle", "progress": ""},
            {"rateLimits": {"primary": {}, "secondary": {"usedPercent": 45}}},
            "ok", "#ffffff", language="en",
        )
        self.assertEqual(snapshot["rows"]["activity"], "Codex Idle")
        self.assertTrue(snapshot["rows"]["weekly"].startswith("Weekly 55% /"))
        self.assertEqual(snapshot["battery"]["remaining_percent"], 55)

    def test_presentation_controller_never_decides_manual_compact_state(self):
        controller = StatusPresentationController()
        snapshot = controller.render(
            {"active": 0, "detail": "Idle", "progress": ""},
            {"rateLimits": {}}, "ok", "#ffffff", language="en",
        )
        self.assertEqual(snapshot["rows"]["activity"], "Codex Idle")
        self.assertFalse(hasattr(controller, "compact"))

    def test_settings_controller_preserves_future_schema_until_explicit_reset(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "future": True})
            path.write_text(original, encoding="utf-8")
            controller = SettingsPersistenceController(path)
            result = controller.load()
            self.assertFalse(result.writable)
            with self.assertRaises(ConfigWriteProtectedError):
                controller.save(DEFAULT_SETTINGS)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            controller.save(DEFAULT_SETTINGS, allow_unsafe_overwrite=True)
            self.assertEqual(controller.schema_status, "current")
            self.assertTrue(controller.writable)

    def test_settings_controller_path_and_backup_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.json"
            second = Path(directory) / "second.json"
            controller = SettingsPersistenceController(first)
            controller.save({**DEFAULT_SETTINGS, "x": 100})
            controller.save({**DEFAULT_SETTINGS, "x": 200})
            self.assertTrue(controller.restore_backup())
            self.assertEqual(controller.load().settings["x"], 100)
            controller.set_path(second)
            self.assertEqual(controller.path, second)
            self.assertEqual(controller.schema_status, "missing")


if __name__ == "__main__":
    unittest.main()
