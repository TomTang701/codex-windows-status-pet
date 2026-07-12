"""Coordinate pure status presentation and compact-mode decisions."""

from __future__ import annotations

from .compact_state_api import CompactState
from .status_snapshot_api import build_status_snapshot, build_tray_error_snapshot


class StatusPresentationController:
    def __init__(self):
        self.compact = CompactState()

    def render(
        self,
        activity,
        quota,
        quota_state,
        font_color,
        compact_enabled,
        hovered,
        blocked,
        battery_quota_source="weekly",
    ):
        snapshot = build_status_snapshot(
            activity,
            quota,
            quota_state,
            font_color,
            battery_quota_source,
        )
        should_compact = self.compact.update(
            compact_enabled, snapshot["active_count"], hovered, blocked
        )
        return snapshot, should_compact

    def force_expanded(self):
        self.compact.force_expanded()

    def render_tray_error(self):
        return build_tray_error_snapshot()
