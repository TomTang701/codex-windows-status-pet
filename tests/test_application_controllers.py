import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.application_controller_api import ApplicationController
from api.settings_persistence_controller_api import SettingsPersistenceController
from api.status_presentation_controller_api import StatusPresentationController
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

    def test_shutdown_prevents_new_generations(self):
        controller = ApplicationController(5)
        controller.shutdown()
        self.assertIsNone(controller.begin_activity())
        self.assertIsNone(controller.begin_quota())

    def test_lifecycle_close_is_idempotent(self):
        lifecycle = WindowLifecycleController()
        self.assertTrue(lifecycle.begin_close())
        self.assertFalse(lifecycle.begin_close())

    def test_presentation_controller_preserves_reset_row(self):
        controller = StatusPresentationController()
        snapshot, compact = controller.render(
            {"active": 1, "detail": "输出中", "progress": "活动对话 1 个"},
            {"rateLimits": {}, "rateLimitResetCredits": {"availableCount": 5}},
            "ok", "#ffffff", True, False, False,
        )
        self.assertEqual(snapshot["rows"]["reset_credit"], "重置 5 次")
        self.assertFalse(compact)

    def test_settings_controller_preserves_future_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "future": True})
            path.write_text(original, encoding="utf-8")
            controller = SettingsPersistenceController(path)
            result = controller.load()
            self.assertFalse(result.writable)
            self.assertFalse(controller.save({"x": 1}))
            self.assertEqual(path.read_text(encoding="utf-8"), original)

