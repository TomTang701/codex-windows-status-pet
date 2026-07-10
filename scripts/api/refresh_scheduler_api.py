"""Single-flight refresh scheduling state, independent from Tk and threads."""

from __future__ import annotations


class RefreshScheduler:
    def __init__(self, interval_seconds=5):
        self.interval_seconds = 5
        self.inflight = False
        self.set_interval(interval_seconds)

    def set_interval(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            value = 5
        self.interval_seconds = min(10, max(1, value))

    def begin(self):
        if self.inflight:
            return False
        self.inflight = True
        return True

    def finish(self):
        self.inflight = False

    @property
    def delay_ms(self):
        return self.interval_seconds * 1000

