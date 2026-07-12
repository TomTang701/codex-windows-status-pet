import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.menu_model_api import build_menu_items


class MenuModelTests(unittest.TestCase):
    def test_english_visible_menu_has_shared_actions_and_live_checks(self):
        items = build_menu_items(
            "en", visible=True, topmost=True, locked=False, compact=True
        )
        self.assertEqual(
            [(item.action, item.label, item.checked) for item in items],
            [
                ("settings", "Settings", None),
                ("topmost", "Always on top", True),
                ("lock", "Lock position", False),
                ("compact", "Compact", True),
                ("hide", "Hide window", None),
                ("exit", "Exit", None),
            ],
        )

    def test_chinese_hidden_menu_uses_show_and_stable_actions(self):
        items = build_menu_items(
            "zh-CN", visible=False, topmost=False, locked=True, compact=False
        )
        self.assertEqual([item.action for item in items], [
            "settings", "topmost", "lock", "compact", "show", "exit",
        ])
        self.assertEqual(items[1].checked, False)
        self.assertEqual(items[2].checked, True)
        self.assertEqual(items[3].checked, False)
        self.assertEqual(items[4].label, "显示窗口")


if __name__ == "__main__":
    unittest.main()
