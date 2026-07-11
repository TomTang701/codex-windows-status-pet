import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_snapshot_api import build_status_snapshot
from api.quota_parse_api import parse_quota_payload
from api.status_rows_api import ROW_IDS


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
        self.assertEqual(tuple(result["rows"]), ("activity", "progress", "primary_5h", "weekly", "reset_credit"))
        self.assertEqual(result["text"], "\n".join(result["rows"].values()))

    def test_stale_state_is_explicit_and_gray(self):
        result = build_status_snapshot({"active": 0}, {"rateLimits": {}}, "stale", "#ffffff")
        self.assertEqual(result["color"], "#9ca3af")
        self.assertIn("额度过期", result["text"])
        self.assertEqual(result["quota_state"], "stale")

    def test_reset_credit_line_contains_time_and_date(self):
        expiry = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {}, "rateLimitResetCredits": {"availableCount": 2, "resetsAt": [expiry]}},
        )
        self.assertRegex(result["text"].splitlines()[-1], r"^重置 2 次 / 18:40 7/12$")

    def test_primary_5h_line_remains_time_only(self):
        reset = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {"usedPercent": 20, "resetsAt": reset}}},
        )
        primary_line = next(line for line in result["text"].splitlines() if line.startswith("5h "))
        self.assertEqual(primary_line, "5h 80% / 18:40")
        self.assertNotIn("7/12", primary_line)

    def test_nested_provider_credit_expiry_reaches_display(self):
        expiry = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        quota = parse_quota_payload({
            "rateLimits": {"primary": {"usedPercent": 20}},
            "rateLimitResetCredits": {
                "availableCount": 5,
                "credits": [{"expiresAt": expiry}],
            },
        })
        result = build_status_snapshot({"active": 0}, quota)
        self.assertEqual(result["text"].splitlines()[-1], "重置 5 次 / 18:40 7/12")

    def test_unavailable_state_uses_approved_rows_without_raw_error(self):
        result = build_status_snapshot(
            {"active": 0, "detail": "空闲", "progress": ""},
            {"rateLimits": {}, "rateLimitResetCredits": {}},
            "unavailable",
            "#ffffff",
        )
        self.assertEqual(result["rows"]["progress"], "额度暂不可用")
        self.assertEqual(result["color"], "#fca5a5")
        self.assertNotIn("transport exploded", result["text"])
        self.assertEqual(tuple(result["rows"]), ROW_IDS)
