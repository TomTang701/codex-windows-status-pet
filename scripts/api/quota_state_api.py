"""Last-good quota state and explicit failure classification."""

from __future__ import annotations

from datetime import datetime, timezone


class QuotaState:
    def __init__(self, stale_after_seconds=30):
        self.state = "loading"
        self.last_good = None
        self.last_success_at = None
        self.last_error = None
        self.stale_after_seconds = max(1, int(stale_after_seconds))

    def update(self, snapshot, now=None):
        self.last_good = snapshot
        self.last_success_at = now or datetime.now(timezone.utc)
        self.last_error = None
        self.state = "ok"
        return self.view()

    def fail(self, error_code="transport_error", now=None):
        now = now or datetime.now(timezone.utc)
        self.last_error = error_code
        if self.last_good is not None and self.last_success_at is not None:
            age = (now - self.last_success_at).total_seconds()
            self.state = "stale" if age > self.stale_after_seconds else "ok"
        else:
            self.state = error_code if error_code in {"signed_out", "unavailable", "protocol_error"} else "unavailable"
        return self.view()

    def view(self):
        return {
            "state": self.state,
            "snapshot": self.last_good,
            "last_success_at": self.last_success_at,
            "error_code": self.last_error,
        }
