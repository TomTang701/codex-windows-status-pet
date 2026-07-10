import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.tray_lifecycle_api import is_known_action, requires_visible_overlay, should_schedule_restart


class TrayLifecycleTests(unittest.TestCase):
    def test_action_allowlist_and_visibility_policy(self):
        self.assertTrue(is_known_action("settings"))
        self.assertFalse(is_known_action("unexpected"))
        self.assertTrue(requires_visible_overlay("settings"))
        self.assertFalse(requires_visible_overlay("hide"))

    def test_tray_restart_is_single_scheduled_and_not_during_close(self):
        self.assertTrue(should_schedule_restart("tray_error"))
        self.assertFalse(should_schedule_restart("tray_error", already_scheduled=True))
        self.assertFalse(should_schedule_restart("tray_error", closing=True))
        self.assertFalse(should_schedule_restart("show"))
