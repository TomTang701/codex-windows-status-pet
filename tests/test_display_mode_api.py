import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_mode_api import compact_size, should_compact
from api.compact_state_api import CompactState, compact_geometry


class DisplayModeTests(unittest.TestCase):
    def test_compact_requires_opt_in_and_idle_pointer(self):
        self.assertFalse(should_compact(False, 0))
        self.assertTrue(should_compact(True, 0))
        self.assertFalse(should_compact(True, 1))
        self.assertFalse(should_compact(True, 0, hovered=True))

    def test_compact_size_is_bounded(self):
        self.assertEqual(compact_size(330, 138), 69)
        self.assertEqual(compact_size("bad", 138), 64)

    def test_compact_waits_for_idle_and_expands_for_activity_or_hover(self):
        state = CompactState(idle_delay_seconds=3)
        self.assertFalse(state.update(True, 0, now=10))
        self.assertFalse(state.update(True, 0, now=12))
        self.assertTrue(state.update(True, 0, now=13))
        self.assertFalse(state.update(True, 1, now=14))
        self.assertFalse(state.update(True, 0, hovered=True, now=15))

    def test_compact_geometry_preserves_bottom_right_anchor(self):
        self.assertEqual(
            compact_geometry(1600, 900, 330, 138, 69, (0, 0, 1920, 1030)),
            (1851, 961),
        )
