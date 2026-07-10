"""Independent, generation-safe refresh channel state."""

from __future__ import annotations

import threading


class RefreshController:
    def __init__(self, channels=("activity", "quota")):
        self._lock = threading.Lock()
        self._generation = {channel: 0 for channel in channels}
        self._inflight = {channel: False for channel in channels}
        self._shutdown = False

    def begin(self, channel):
        with self._lock:
            if self._shutdown or channel not in self._inflight or self._inflight[channel]:
                return None
            self._inflight[channel] = True
            self._generation[channel] += 1
            return self._generation[channel]

    def is_current(self, channel, generation):
        with self._lock:
            return (
                not self._shutdown
                and channel in self._generation
                and self._inflight.get(channel, False)
                and self._generation[channel] == generation
            )

    def finish(self, channel, generation):
        with self._lock:
            if channel not in self._inflight or self._generation[channel] != generation:
                return False
            self._inflight[channel] = False
            return True

    def cancel(self, channel):
        with self._lock:
            if channel not in self._generation:
                return False
            self._generation[channel] += 1
            self._inflight[channel] = False
            return True

    def shutdown(self):
        with self._lock:
            self._shutdown = True
            for channel in self._generation:
                self._generation[channel] += 1
                self._inflight[channel] = False

    @property
    def is_shutdown(self):
        with self._lock:
            return self._shutdown
