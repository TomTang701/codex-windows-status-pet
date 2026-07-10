import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_parse_api import parse_quota_payload


class QuotaParseTests(unittest.TestCase):
    def test_only_approved_fields_are_normalized(self):
        result = parse_quota_payload({
            "rateLimits": {"primary": {"usedPercent": 20, "secret": "drop"}},
            "rateLimitResetCredits": {"availableCount": 4, "secret": "drop"},
            "token": "must-not-propagate",
        })
        self.assertEqual(result["rateLimits"]["primary"], {"usedPercent": 20})
        self.assertEqual(result["rateLimitResetCredits"], {"availableCount": 4})
        self.assertNotIn("token", result)

    def test_snake_case_aliases_and_invalid_numbers(self):
        result = parse_quota_payload({
            "rate_limits": {"primary": {"used_percent": "bad", "resets_at": 123}},
            "rate_limit_reset_credits": {"available_count": 2, "resetAt": ["2030-01-01T00:00:00Z"]},
        })
        self.assertEqual(result["rateLimits"]["primary"], {"resetsAt": 123})
        self.assertEqual(result["rateLimitResetCredits"]["resetsAt"], ["2030-01-01T00:00:00Z"])
