"""Admission contract for physical mixed-DPI host tests."""

import unittest

from tests.test_ui_mixed_dpi_startup_position import topology_from_monitors


class MixedDpiTopologyAdmissionTests(unittest.TestCase):
    def test_required_primary_and_right_side_secondary_are_admitted(self):
        primary, secondary = topology_from_monitors([
            {"name": "primary", "work": [0, 0, 2560, 1380], "dpi_x": 120},
            {"name": "secondary", "work": [2560, 354, 4480, 1386], "dpi_x": 96},
        ])
        self.assertEqual(primary["dpi_x"], 120)
        self.assertEqual(secondary["dpi_x"], 96)

    def test_missing_right_side_secondary_skips_with_required_topology_reason(self):
        with self.assertRaisesRegex(unittest.SkipTest, "required 125% primary / 100% right-side secondary topology unavailable"):
            topology_from_monitors([{"name": "primary", "work": [0, 0, 1920, 1040], "dpi_x": 96}])


if __name__ == "__main__":
    unittest.main()
