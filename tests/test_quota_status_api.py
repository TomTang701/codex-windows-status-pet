import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_status_api import health_tier, remaining_percent


class QuotaStatusTests(unittest.TestCase):
    def test_health_tiers(self):
        self.assertEqual(remaining_percent({"usedPercent": 20}), 80.0)
        self.assertEqual(health_tier({"usedPercent": 20}), "healthy")
        self.assertEqual(health_tier({"usedPercent": 60}), "caution")
        self.assertEqual(health_tier({"usedPercent": 95}), "critical")

    def test_invalid_window_is_unavailable(self):
        self.assertIsNone(remaining_percent({"usedPercent": "bad"}))
        self.assertEqual(health_tier(None), "unavailable")
