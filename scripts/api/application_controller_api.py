"""Application-level coordination for independent refresh channels."""

from __future__ import annotations

from .refresh_controller_api import RefreshController
from .refresh_scheduler_api import RefreshScheduler


class ApplicationController:
    def __init__(self, quota_interval):
        self.refresh = RefreshController(("activity", "quota"))
        self.quota = RefreshScheduler(quota_interval)

    def set_quota_interval(self, seconds):
        self.quota.set_interval(seconds)

    def begin_activity(self):
        return self.refresh.begin("activity")

    def begin_quota(self):
        if not self.quota.begin():
            return None
        generation = self.refresh.begin("quota")
        if generation is None:
            self.quota.finish()
        return generation

    def finish(self, channel, generation):
        self.refresh.finish(channel, generation)
        if channel == "quota":
            self.quota.finish()

    def is_current(self, channel, generation):
        return self.refresh.is_current(channel, generation)

    @property
    def quota_delay_ms(self):
        return self.quota.delay_ms

    def shutdown(self):
        self.refresh.shutdown()
