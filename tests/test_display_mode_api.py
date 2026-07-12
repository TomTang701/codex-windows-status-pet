import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_mode_api import compact_size
from api.compact_state_api import compact_geometry


class DisplayModeTests(unittest.TestCase):
    def test_compact_size_is_bounded(self):
        self.assertEqual(compact_size(330, 138), 69)
        self.assertEqual(compact_size("bad", 138), 64)

    def test_compact_geometry_preserves_bottom_right_anchor(self):
        self.assertEqual(
            compact_geometry(1600, 900, 330, 138, 69, (0, 0, 1920, 1030)),
            (1851, 961),
        )
