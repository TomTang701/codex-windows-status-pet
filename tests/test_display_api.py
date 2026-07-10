import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_api import place_popup, rectangle_intersects_virtual_desktop, scale_for_dpi, work_area_for_point


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

    def test_popup_is_fully_inside_bottom_right_work_area(self):
        position = place_popup(1910, 1060, 240, 220, (0, 0, 1920, 1080))
        self.assertGreaterEqual(position[0], 0)
        self.assertGreaterEqual(position[1], 0)
        self.assertLessEqual(position[0] + 240, 1920)
        self.assertLessEqual(position[1] + 220, 1080)

    def test_work_area_uses_secondary_monitor_for_virtual_point(self):
        monitors = [
            {"work": [0, 0, 1920, 1080]},
            {"work": [2560, 300, 4480, 1434]},
        ]
        self.assertEqual(work_area_for_point(4151, 1248, monitors), (2560, 300, 4480, 1434))


if __name__ == "__main__":
    unittest.main()
