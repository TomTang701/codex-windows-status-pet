"""Time-aware compact/expanded state decisions."""

from __future__ import annotations

import time


class CompactState:
    def __init__(self, idle_delay_seconds=3.0, clock=None):
        self.idle_delay_seconds = max(0.0, float(idle_delay_seconds))
        self.clock = clock or time.monotonic
        self.idle_since = None
        self.compact = False

    def update(self, enabled, active_count, hovered=False, blocked=False, now=None):
        now = self.clock() if now is None else float(now)
        if not enabled or int(active_count or 0) > 0 or hovered or blocked:
            self.idle_since = None
            self.compact = False
            return self.compact
        if self.idle_since is None:
            self.idle_since = now
        if now - self.idle_since >= self.idle_delay_seconds:
            self.compact = True
        return self.compact

    def force_expanded(self):
        self.idle_since = None
        self.compact = False


def compact_geometry(x, y, expanded_width, expanded_height, compact_size, work_area, margin=8):
    """Keep the compact orb anchored to the right/bottom edge when applicable."""
    left, top, right, bottom = work_area
    x = int(x)
    y = int(y)
    size = int(compact_size)
    if x + int(expanded_width) >= right - margin:
        x = x + int(expanded_width) - size
    if y + int(expanded_height) >= bottom - margin:
        y = y + int(expanded_height) - size
    return min(max(x, left), max(left, right - size)), min(max(y, top), max(top, bottom - size))
