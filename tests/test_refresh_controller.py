import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.refresh_controller_api import RefreshController


class RefreshControllerTests(unittest.TestCase):
    def test_channels_are_independent_single_flight(self):
        controller = RefreshController()
        activity_generation = controller.begin("activity")
        self.assertIsNotNone(activity_generation)
        self.assertIsNotNone(controller.begin("quota"))
        self.assertIsNone(controller.begin("activity"))
        self.assertTrue(controller.finish("activity", activity_generation))

    def test_stale_generation_cannot_finish_new_work(self):
        controller = RefreshController()
        old_generation = controller.begin("quota")
        controller.cancel("quota")
        new_generation = controller.begin("quota")
        self.assertNotEqual(old_generation, new_generation)
        self.assertFalse(controller.finish("quota", old_generation))
        self.assertTrue(controller.is_current("quota", new_generation))

    def test_shutdown_invalidates_callbacks_and_new_work(self):
        controller = RefreshController()
        generation = controller.begin("activity")
        controller.shutdown()
        self.assertTrue(controller.is_shutdown)
        self.assertFalse(controller.is_current("activity", generation))
        self.assertIsNone(controller.begin("quota"))
