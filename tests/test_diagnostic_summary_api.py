import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.diagnostic_summary_api import build_diagnostic_summary


class DiagnosticSummaryTests(unittest.TestCase):
    def test_summary_contains_operational_state_without_sensitive_payloads(self):
        with tempfile.TemporaryDirectory() as directory:
            activity = Path(directory) / "sessions"
            activity.mkdir()
            result = build_diagnostic_summary(
                version="0.2.0",
                settings_path=Path(directory) / "settings.json",
                log_path=Path(directory) / "pet.log",
                activity_path=activity,
                app_server_running=True,
                quota_state="stale",
                monitor_count=2,
                dpi=144,
                now=datetime(2030, 1, 1, tzinfo=timezone.utc),
            )
            self.assertIn("app_server=running", result)
            self.assertIn("quota_state=stale", result)
            self.assertIn("monitor_count=2", result)
            self.assertIn("activity_path_exists=True", result)
            self.assertIn("sensitive_data=excluded", result)
            self.assertNotIn("access_token", result)
            self.assertNotIn("rateLimits", result)

    def test_missing_paths_are_reported_as_false_or_unset(self):
        result = build_diagnostic_summary("0.2.0", None, None, None, False, "loading", 0, 0)
        self.assertIn("activity_path_exists=False", result)
        self.assertIn("settings_path=<unset>", result)
