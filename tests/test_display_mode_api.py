import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_mode_api import compact_size, should_compact


class DisplayModeTests(unittest.TestCase):
    def test_compact_requires_opt_in_and_idle_pointer(self):
        self.assertFalse(should_compact(False, 0))
        self.assertTrue(should_compact(True, 0))
        self.assertFalse(should_compact(True, 1))
        self.assertFalse(should_compact(True, 0, hovered=True))

    def test_compact_size_is_bounded(self):
        self.assertEqual(compact_size(330, 138), 69)
        self.assertEqual(compact_size("bad", 138), 64)
