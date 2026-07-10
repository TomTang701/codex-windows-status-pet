import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.window_recovery_api import recover_position


class WindowRecoveryTests(unittest.TestCase):
    monitors = [
        {"work": [-1920, 0, 0, 1080]},
        {"work": [0, 0, 1920, 1080]},
        {"work": [2560, 0, 4480, 1080]},
    ]

    def test_legal_secondary_and_negative_positions_are_preserved(self):
        self.assertEqual(recover_position(4151, 100, 330, 138, self.monitors)[:2], (4151, 100))
        self.assertEqual(recover_position(-1800, 100, 330, 138, self.monitors)[:2], (-1800, 100))

    def test_disconnected_position_recovers_to_nearest_monitor(self):
        x, y, recovered = recover_position(2200, 900, 330, 138, self.monitors)
        self.assertTrue(recovered)
        self.assertEqual((x, y), (1590, 900))

    def test_partially_taskbar_covered_window_is_repositioned(self):
        monitors = [{"work": [0, 0, 1920, 1000]}]
        x, y, recovered = recover_position(100, 950, 330, 138, monitors)
        self.assertTrue(recovered)
        self.assertEqual((x, y), (100, 862))

    def test_fully_contained_window_is_not_moved(self):
        x, y, recovered = recover_position(4151, 100, 330, 138, self.monitors)
        self.assertEqual((x, y, recovered), (4151, 100, False))
