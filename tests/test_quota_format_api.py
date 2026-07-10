import unittest
from datetime import datetime
from unittest.mock import patch

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_format_api import earliest_future_expiry, quota_line, reset_credit_line


class QuotaFormatTests(unittest.TestCase):
    def test_earliest_future_expiry_ignores_invalid_and_past_values(self):
        self.assertEqual(
            earliest_future_expiry([{"expiresAt": "90"}, {"expiresAt": "120"}, {"expiresAt": "bad"}], now=100),
            120.0,
        )

    def test_earliest_expiry_accepts_iso_reset_field(self):
        self.assertEqual(
            earliest_future_expiry({"items": [{"resetsAt": "1970-01-01T00:02:00Z"}]}, now=100),
            120.0,
        )

    def test_dates_have_no_leading_zero(self):
        timestamp = datetime(2026, 7, 10, 15, 16).astimezone().timestamp()
        with patch("api.quota_format_api.datetime") as mocked:
            mocked.fromtimestamp.side_effect = datetime.fromtimestamp
            mocked.now.side_effect = datetime.now
            line = quota_line("周", "85%", timestamp)
        self.assertRegex(line, r"^周 85% / 15:16 7/10$")

    def test_missing_reset_time_is_not_invented(self):
        self.assertEqual(reset_credit_line(5, None), "重置 5 次")


if __name__ == "__main__":
    unittest.main()
