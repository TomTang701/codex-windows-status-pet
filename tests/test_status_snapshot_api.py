import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_snapshot_api import battery_presentation, build_status_snapshot
from api.quota_parse_api import parse_quota_payload
from api.status_rows_api import ROW_IDS


class StatusSnapshotTests(unittest.TestCase):
    def test_each_selected_source_uses_only_its_own_real_quota(self):
        quota = {
            "rateLimits": {
                "primary": {"usedPercent": 20},
                "secondary": {"usedPercent": 45},
            }
        }
        expected = {
            "primary_5h": (80, 8),
            "weekly": (55, 6),
        }
        for source, (remaining, segments) in expected.items():
            with self.subTest(source=source):
                result = build_status_snapshot(
                    {"active": 0}, quota, battery_quota_source=source
                )
                self.assertEqual(result["battery"]["remaining_percent"], remaining)
                self.assertEqual(result["battery"]["lit_segments"], segments)

    def test_selected_weekly_remains_available_when_primary_is_absent(self):
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {}, "secondary": {"usedPercent": 45}}},
            battery_quota_source="weekly",
        )
        self.assertTrue(result["battery"]["available"])
        self.assertEqual(result["battery"]["remaining_percent"], 55)

    def test_selected_primary_battery_never_reads_weekly(self):
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {}, "secondary": {"usedPercent": 45}}},
            battery_quota_source="primary_5h",
        )
        self.assertFalse(result["battery"]["available"])

    def test_weekly_only_window_keeps_5h_unavailable_and_drives_battery(self):
        reset = datetime(2030, 7, 12, 18, 40).astimezone().timestamp()
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {}, "secondary": {"usedPercent": 45, "resetsAt": reset}}},
        )
        self.assertEqual(result["rows"]["primary_5h"], "5h -- / --")
        self.assertTrue(result["rows"]["weekly"].startswith("周 55% /"))
        self.assertEqual(result["battery"]["remaining_percent"], 55)

    def test_weekly_battery_never_falls_back_to_available_5h(self):
        result = build_status_snapshot(
            {"active": 0},
            {"rateLimits": {"primary": {"usedPercent": 20}, "secondary": {}}},
        )
        self.assertFalse(result["battery"]["available"])

    def test_battery_presentation_uses_remaining_ceiling_segments(self):
        expected = {
            0: 0, 1: 1, 9: 1, 10: 1, 11: 2, 20: 2, 21: 3,
            60: 6, 61: 7, 70: 7, 71: 8, 78: 8, 80: 8,
            81: 9, 90: 9, 91: 10, 100: 10,
        }
        for remaining, segments in expected.items():
            with self.subTest(remaining=remaining):
                result = battery_presentation({"usedPercent": 100 - remaining})
                self.assertTrue(result["available"])
                self.assertEqual(result["remaining_percent"], remaining)
                self.assertEqual(result["lit_segments"], segments)

    def test_battery_presentation_has_ten_ordered_fixed_color_cells(self):
        result = battery_presentation({"usedPercent": 22})
        self.assertEqual(len(result["segments"]), 10)
        self.assertEqual([segment["index"] for segment in result["segments"]], list(range(1, 11)))
        self.assertEqual([segment["lit"] for segment in result["segments"]], [True] * 8 + [False] * 2)
        self.assertEqual(len({segment["color"] for segment in result["segments"][0:2]}), 1)
        self.assertEqual(len({segment["color"] for segment in result["segments"][2:4]}), 1)
        self.assertEqual(len({segment["color"] for segment in result["segments"][4:6]}), 1)
        self.assertEqual(len({segment["color"] for segment in result["segments"][6:8]}), 1)
        self.assertEqual(len({segment["color"] for segment in result["segments"][8:10]}), 1)
        self.assertNotEqual(result["segments"][6]["color"], result["segments"][8]["color"])

    def test_battery_presentation_distinguishes_unavailable_from_known_empty(self):
        self.assertFalse(battery_presentation({})["available"])
        self.assertEqual(battery_presentation({"usedPercent": 100})["lit_segments"], 0)

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

    def test_language_changes_visible_status_text_without_changing_row_or_battery_identity(self):
        quota = {
            "rateLimits": {"primary": {}, "secondary": {"usedPercent": 45}},
            "rateLimitResetCredits": {"availableCount": 5},
        }
        english = build_status_snapshot(
            {"active": 0, "detail": "Idle", "progress": ""},
            quota,
            "unavailable",
            "#ffffff",
            language="en",
        )
        chinese = build_status_snapshot(
            {"active": 0, "detail": "空闲", "progress": ""},
            quota,
            "unavailable",
            "#ffffff",
            language="zh-CN",
        )
        self.assertEqual(english["rows"]["activity"], "Codex Idle")
        self.assertEqual(chinese["rows"]["activity"], "Codex 空闲")
        self.assertEqual(english["rows"]["progress"], "Quota unavailable")
        self.assertEqual(chinese["rows"]["progress"], "额度暂不可用")
        self.assertTrue(english["rows"]["weekly"].startswith("Week 55% /"))
        self.assertTrue(chinese["rows"]["weekly"].startswith("周 55% /"))
        self.assertTrue(english["rows"]["reset_credit"].startswith("Reset 5 times"))
        self.assertTrue(chinese["rows"]["reset_credit"].startswith("重置 5 次"))
        self.assertEqual(tuple(english["rows"]), ROW_IDS)
        self.assertEqual(english["battery"], chinese["battery"])
