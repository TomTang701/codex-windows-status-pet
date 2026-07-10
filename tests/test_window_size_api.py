import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.window_size_api import resize_dimensions


class WindowSizeTests(unittest.TestCase):
    def test_free_resize_changes_width_only(self):
        self.assertEqual(resize_dimensions(330, 138, 1.1), (363, 138))

    def test_proportional_resize_changes_both_dimensions(self):
        self.assertEqual(resize_dimensions(330, 138, 1.1, proportional=True), (363, 152))

    def test_resize_is_bounded_and_rejects_invalid_factor(self):
        self.assertEqual(resize_dimensions(1000, 700, 2, proportional=True), (1200, 800))
        with self.assertRaises(ValueError):
            resize_dimensions(330, 138, 0)
