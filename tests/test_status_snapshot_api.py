import sys
import unittest
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
