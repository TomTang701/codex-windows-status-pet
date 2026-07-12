"""Pure presentation snapshot for the overlay status text and color."""

from __future__ import annotations

from datetime import datetime, timezone

try:
    from api.quota_format_api import quota_line, reset_credit_line, earliest_future_expiry
    from api.quota_status_api import HEALTH_COLORS, health_tier
    from api.status_rows_api import StatusRowsSnapshot
    from api.localization_api import translate
except ModuleNotFoundError:
    from scripts.api.quota_format_api import quota_line, reset_credit_line, earliest_future_expiry
    from scripts.api.quota_status_api import HEALTH_COLORS, health_tier
    from scripts.api.status_rows_api import StatusRowsSnapshot
    from scripts.api.localization_api import translate


ERROR_COLOR = "#fca5a5"
BATTERY_SEGMENT_COLORS = (
    "#ef4444", "#ef4444",
    "#f97316", "#f97316",
    "#facc15", "#facc15",
    "#a3e635", "#a3e635",
    "#22c55e", "#22c55e",
)


def _percent_left(window):
    if not isinstance(window, dict) or "usedPercent" not in window:
        return "--"
    try:
        used = int(window.get("usedPercent", 0))
    except (TypeError, ValueError):
        return "--"
    return f"{max(0, 100 - used)}%"


def _short_time(epoch):
    if not epoch:
        return "--"
    try:
        return datetime.fromtimestamp(float(epoch), tz=timezone.utc).astimezone().strftime("%H:%M")
    except (TypeError, ValueError, OverflowError, OSError):
        return "--"


def battery_presentation(window):
    """Return one truthful remaining-quota state for expanded and compact battery views."""
    remaining = _percent_left(window)
    if remaining == "--":
        return {
            "available": False,
            "remaining_percent": None,
            "lit_segments": None,
            "segments": tuple(
                {"index": index, "lit": False, "color": color}
                for index, color in enumerate(BATTERY_SEGMENT_COLORS, start=1)
            ),
        }
    value = int(remaining[:-1])
    lit_segments = 0 if value == 0 else min(10, (value + 9) // 10)
    return {
        "available": True,
        "remaining_percent": value,
        "lit_segments": lit_segments,
        "segments": tuple(
            {"index": index, "lit": index <= lit_segments, "color": color}
            for index, color in enumerate(BATTERY_SEGMENT_COLORS, start=1)
        ),
    }
def build_status_snapshot(
    activity,
    quota,
    quota_state="loading",
    font_color="#e5e7eb",
    battery_quota_source="weekly",
    language="zh-CN",
):
    """Build only approved display text; raw quota/activity payloads never escape."""
    activity = activity if isinstance(activity, dict) else {}
    quota = quota if isinstance(quota, dict) else {}
    limits = quota.get("rateLimits", {})
    limits = limits if isinstance(limits, dict) else {}
    primary = limits.get("primary", {})
    secondary = limits.get("secondary", {})
    primary = primary if isinstance(primary, dict) else {}
    secondary = secondary if isinstance(secondary, dict) else {}
    credits = quota.get("rateLimitResetCredits") or {}
    credit_items = credits if isinstance(credits, (list, dict)) else []
    tier = health_tier(primary)
    if quota_state == "stale":
        color = "#9ca3af"
    elif quota_state == "unavailable":
        color = ERROR_COLOR
    else:
        color = font_color if tier == "healthy" else HEALTH_COLORS.get(tier, font_color)
    state_label = translate(language, "stale") if quota_state == "stale" else ""
    active_count = int(activity.get("active", 0) or 0)
    rows = StatusRowsSnapshot(
        activity=translate(language, "activity", detail=activity.get("detail", translate(language, "idle"))) + state_label,
        progress=translate(language, "quota_unavailable") if quota_state == "unavailable" else activity.get("progress", ""),
        primary_5h=f"5h {_percent_left(primary)} / {_short_time(primary.get('resetsAt'))}",
        weekly=quota_line(translate(language, "week"), _percent_left(secondary), secondary.get("resetsAt")),
        reset_credit=reset_credit_line(
            credits.get("availableCount", "--") if isinstance(credits, dict) else "--",
            earliest_future_expiry(credit_items),
        ),
    )
    selected_window = primary if battery_quota_source == "primary_5h" else secondary
    return {
        "text": rows.as_text(),
        "rows": rows.as_dict(),
        "battery": battery_presentation(selected_window),
        "color": color,
        "active_count": active_count,
        "quota_tier": tier,
        "quota_state": quota_state,
    }


def build_tray_error_snapshot(language="zh-CN"):
    """Return the approved five-row presentation for tray failure."""
    rows = StatusRowsSnapshot("Codex", translate(language, "tray_error"), "", "", "")
    return {
        "text": rows.as_text(),
        "rows": rows.as_dict(),
        "color": ERROR_COLOR,
        "active_count": 0,
        "quota_tier": "unavailable",
        "quota_state": "tray_error",
    }
