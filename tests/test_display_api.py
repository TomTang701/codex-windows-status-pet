import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_api import rectangle_intersects_virtual_desktop, scale_for_dpi


class DisplayApiTests(unittest.TestCase):
    def test_mixed_dpi_scale_values_are_deterministic(self):
        self.assertEqual(scale_for_dpi(96), 1.0)
        self.assertEqual(scale_for_dpi(144), 1.5)
        self.assertEqual(scale_for_dpi(192), 2.0)

    def test_virtual_desktop_intersection_preserves_legal_coordinates(self):
        bounds = (0, 0, 4480, 1434)
        self.assertTrue(rectangle_intersects_virtual_desktop(4151, 1248, 330, 138, bounds))
        self.assertFalse(rectangle_intersects_virtual_desktop(5000, 2000, 330, 138, bounds))
        self.assertTrue(rectangle_intersects_virtual_desktop(-200, 50, 330, 138, bounds))


if __name__ == "__main__":
    unittest.main()
