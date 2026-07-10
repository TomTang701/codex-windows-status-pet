import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_provider_api import normalize_snapshot


class QuotaProviderTests(unittest.TestCase):
    def test_normalizes_valid_local_response(self):
        result = normalize_snapshot({
            "rateLimits": {"primary": {"usedPercent": 20}},
            "rateLimitResetCredits": {"availableCount": 4},
            "unexpected": "ignored",
        })
        self.assertEqual(result["status"], "available")
        self.assertEqual(result["rateLimitResetCredits"]["availableCount"], 4)
        self.assertNotIn("unexpected", result)

    def test_invalid_response_is_unavailable_without_credentials(self):
        result = normalize_snapshot({"rateLimits": "bad", "token": "must-not-propagate"})
        self.assertEqual(result, {"status": "unavailable", "rateLimits": {}, "rateLimitResetCredits": {}})
