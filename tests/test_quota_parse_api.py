import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_parse_api import parse_quota_payload


class QuotaParseTests(unittest.TestCase):
    def test_approved_local_fields_are_normalized_and_unknown_fields_are_dropped(self):
        result = parse_quota_payload({
            "rateLimits": {"primary": {"usedPercent": 20}},
            "rateLimitResetCredits": {"availableCount": 4},
            "unexpected": "ignored",
        })
        self.assertEqual(result["status"], "available")
        self.assertEqual(result["rateLimitResetCredits"]["availableCount"], 4)
        self.assertNotIn("unexpected", result)

    def test_malformed_payload_is_unavailable_without_propagating_credentials(self):
        result = parse_quota_payload({"rateLimits": "bad", "token": "must-not-propagate"})
        self.assertEqual(result, {"status": "unavailable", "rateLimits": {}, "rateLimitResetCredits": {}})

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

    def test_reset_credit_expiry_shapes_are_normalized(self):
        cases = (
            ({"resetsAt": [1893456000]}, [1893456000]),
            ({"resetAt": "2030-01-01T00:00:00Z"}, ["2030-01-01T00:00:00Z"]),
            ({"expirations": [{"expiresAt": 1893456000}]}, [1893456000]),
            ({"credits": [{"expires_at": "2030-01-01T00:00:00Z"}]}, ["2030-01-01T00:00:00Z"]),
            ({"resets_at": [1893456000]}, [1893456000]),
        )
        for credits, expected in cases:
            with self.subTest(credits=credits):
                result = parse_quota_payload({
                    "rateLimits": {"primary": {"usedPercent": 20}},
                    "rateLimitResetCredits": credits,
                })
                self.assertEqual(result["rateLimitResetCredits"]["resetsAt"], expected)

    def test_unknown_and_credential_fields_never_propagate(self):
        result = parse_quota_payload({
            "rateLimits": {"primary": {"usedPercent": 20}},
            "rateLimitResetCredits": {
                "availableCount": 2,
                "expirations": [{"expiresAt": 1893456000, "token": "drop"}],
                "auth": {"expiresAt": 1893457000},
                "unknown": {"resetAt": 1893458000},
            },
        })
        self.assertEqual(result["rateLimitResetCredits"], {"availableCount": 2, "resetsAt": [1893456000]})
        self.assertNotIn("token", repr(result))

    def test_damaged_expiry_objects_are_ignored(self):
        result = parse_quota_payload({
            "rateLimits": {"primary": {"usedPercent": 20}},
            "rateLimitResetCredits": {"expirations": [None, True, {}, {"expiresAt": []}]},
        })
        self.assertEqual(result["rateLimitResetCredits"], {})
