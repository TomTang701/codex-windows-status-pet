import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_snapshot_api import build_status_snapshot


class StatusSnapshotTests(unittest.TestCase):
    def test_snapshot_formats_only_display_fields(self):
        result = build_status_snapshot(
            {"detail": "工具调用", "progress": "活动对话 1 个", "active": 1},
            {"rateLimits": {"primary": {"usedPercent": 20, "resetsAt": 1893456000}, "secondary": {}},
             "rateLimitResetCredits": {"availableCount": 2}, "secret": "drop"},
            font_color="#ffffff",
        )
        self.assertIn("Codex 工具调用", result["text"])
        self.assertIn("活动对话 1 个", result["text"])
        self.assertEqual(result["active_count"], 1)
        self.assertEqual(result["quota_tier"], "healthy")
        self.assertNotIn("secret", result["text"])

    def test_stale_state_is_explicit_and_gray(self):
        result = build_status_snapshot({"active": 0}, {"rateLimits": {}}, "stale", "#ffffff")
        self.assertEqual(result["color"], "#9ca3af")
        self.assertIn("额度过期", result["text"])
        self.assertEqual(result["quota_state"], "stale")

    def test_snapshot_reset_credit_line_contains_time_and_date(self):
        expiry = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {}, "rateLimitResetCredits": {"availableCount": 2, "resetsAt": [expiry]}},
        )
        self.assertRegex(result["text"].splitlines()[-1], r"^重置 2 次 / 18:40 7/12$")
        self.assertRegex(result["rows"]["reset_credit"], r"^重置 2 次 / 18:40 7/12$")
        self.assertEqual(tuple(result["rows"]), ("activity", "progress", "primary_5h", "weekly", "reset_credit"))

    def test_snapshot_primary_5h_line_contains_time_only(self):
        reset = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {"usedPercent": 20, "resetsAt": reset}}},
        )
        primary_line = next(line for line in result["text"].splitlines() if line.startswith("5h "))
        self.assertEqual(primary_line, "5h 80% / 18:40")
        self.assertNotIn("7/12", primary_line)

    def test_snapshot_does_not_expose_raw_provider_fields(self):
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {}, "rateLimitResetCredits": {"availableCount": 2, "resetsAt": [], "token": "drop"}},
        )
        self.assertNotIn("token", result["text"])
        self.assertNotIn("drop", result["text"])
