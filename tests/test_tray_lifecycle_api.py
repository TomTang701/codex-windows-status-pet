import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.tray_lifecycle_api import is_known_action, requires_visible_overlay, should_schedule_restart
from ui.tray_adapter import TrayIcon3, tray_menu_items


class TrayLifecycleTests(unittest.TestCase):
    def test_tray_menu_consumes_shared_state_model(self):
        visible = tray_menu_items("en", visible=True, topmost=True, locked=False, compact=True)
        hidden = tray_menu_items("zh-CN", visible=False, topmost=False, locked=True, compact=False)
        self.assertEqual([item.action for item in visible], ["settings", "topmost", "lock", "compact", "hide", "exit"])
        self.assertEqual([item.checked for item in visible], [None, True, False, True, None, None])
        self.assertEqual([item.action for item in hidden], ["settings", "topmost", "lock", "compact", "show", "exit"])
        self.assertEqual(hidden[4].label, "显示窗口")
    def test_action_allowlist_and_visibility_policy(self):
        self.assertTrue(is_known_action("settings"))
        self.assertTrue(is_known_action("topmost"))
        self.assertTrue(is_known_action("lock"))
        self.assertTrue(is_known_action("compact"))
        self.assertFalse(is_known_action("unexpected"))
        self.assertTrue(requires_visible_overlay("settings"))
        self.assertFalse(requires_visible_overlay("hide"))

    def test_tray_restart_is_single_scheduled_and_not_during_close(self):
        self.assertTrue(should_schedule_restart("tray_error"))
        self.assertFalse(should_schedule_restart("tray_error", already_scheduled=True))
        self.assertFalse(should_schedule_restart("tray_error", closing=True))
        self.assertFalse(should_schedule_restart("show"))

    def test_tray_stop_is_idempotent(self):
        tray = TrayIcon3.__new__(TrayIcon3)
        tray._stopped = False

        class FakeIcon:
            def __init__(self):
                self.calls = 0

            def stop(self):
                self.calls += 1

        tray.icon = FakeIcon()
        tray.stop()
        tray.stop()
        self.assertEqual(tray.icon.calls, 1)

    def test_language_update_reuses_existing_tray_icon(self):
        tray = TrayIcon3.__new__(TrayIcon3)

        class FakeIcon:
            menu = None

        tray.icon = FakeIcon()
        tray.set_language("zh-CN")
        self.assertEqual(tray.language, "zh-CN")
        self.assertIsNotNone(tray.icon.menu)
