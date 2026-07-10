import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.refresh_scheduler_api import RefreshScheduler


class RefreshSchedulerTests(unittest.TestCase):
    def test_single_flight_and_bounded_delay(self):
        scheduler = RefreshScheduler(99)
        self.assertEqual(scheduler.delay_ms, 10000)
        self.assertTrue(scheduler.begin())
        self.assertFalse(scheduler.begin())
        scheduler.finish()
        self.assertTrue(scheduler.begin())

    def test_invalid_interval_falls_back(self):
        scheduler = RefreshScheduler("bad")
        self.assertEqual(scheduler.delay_ms, 5000)
        scheduler.set_interval(0)
        self.assertEqual(scheduler.delay_ms, 1000)
