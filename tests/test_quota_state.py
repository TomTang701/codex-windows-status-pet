import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.quota_state_api import QuotaState


class QuotaStateTests(unittest.TestCase):
    def test_loading_success_and_recent_failure_keep_last_good(self):
        state = QuotaState(stale_after_seconds=30)
        now = datetime(2030, 1, 1, tzinfo=timezone.utc)
        snapshot = {"rateLimits": {"primary": {"usedPercent": 10}}}
        self.assertEqual(state.state, "loading")
        state.update(snapshot, now)
        self.assertEqual(state.state, "ok")
        state.fail("transport_error", now + timedelta(seconds=10))
        self.assertEqual(state.state, "ok")
        self.assertIs(state.last_good, snapshot)

    def test_old_failure_becomes_stale_and_no_data_is_unavailable(self):
        state = QuotaState(stale_after_seconds=30)
        now = datetime(2030, 1, 1, tzinfo=timezone.utc)
        state.update({"value": 1}, now)
        state.fail("transport_error", now + timedelta(seconds=31))
        self.assertEqual(state.state, "stale")
        empty = QuotaState()
        empty.fail("protocol_error", now)
        self.assertEqual(empty.state, "protocol_error")
