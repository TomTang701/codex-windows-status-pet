"""Coordinate pure status presentation and compact-mode decisions."""

from __future__ import annotations

from .status_snapshot_api import build_status_snapshot, build_tray_error_snapshot


class StatusPresentationController:
    def render(
        self,
        activity,
        quota,
        quota_state,
        font_color,
        battery_quota_source="weekly",
        language="zh-CN",
    ):
        snapshot = build_status_snapshot(
            activity,
            quota,
            quota_state,
            font_color,
            battery_quota_source,
            language,
        )
        return snapshot

    def render_tray_error(self, language="zh-CN"):
        return build_tray_error_snapshot(language)
