"""Pure presentation snapshot for the overlay status text and color."""

from __future__ import annotations

from datetime import datetime, timezone

try:
    from api.quota_format_api import quota_line, reset_credit_line, earliest_future_expiry
    from api.quota_status_api import HEALTH_COLORS, health_tier
    from api.status_rows_api import StatusRowsSnapshot
except ModuleNotFoundError:
    from scripts.api.quota_format_api import quota_line, reset_credit_line, earliest_future_expiry
    from scripts.api.quota_status_api import HEALTH_COLORS, health_tier
    from scripts.api.status_rows_api import StatusRowsSnapshot


ERROR_COLOR = "#fca5a5"


def _percent_left(window):
    if not isinstance(window, dict):
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


def build_status_snapshot(activity, quota, quota_state="loading", font_color="#e5e7eb"):
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
    state_label = "（额度过期）" if quota_state == "stale" else ""
    active_count = int(activity.get("active", 0) or 0)
    rows = StatusRowsSnapshot(
        activity=f"Codex {activity.get('detail', '空闲')}{state_label}",
        progress="额度暂不可用" if quota_state == "unavailable" else activity.get("progress", ""),
        primary_5h=f"5h {_percent_left(primary)} / {_short_time(primary.get('resetsAt'))}",
        weekly=quota_line("周", _percent_left(secondary), secondary.get("resetsAt")),
        reset_credit=reset_credit_line(
            credits.get("availableCount", "--") if isinstance(credits, dict) else "--",
            earliest_future_expiry(credit_items),
        ),
    )
    return {
        "text": rows.as_text(),
        "rows": rows.as_dict(),
        "color": color,
        "active_count": active_count,
        "quota_tier": tier,
        "quota_state": quota_state,
    }


def build_tray_error_snapshot():
    """Return the approved five-row presentation for tray failure."""
    rows = StatusRowsSnapshot("Codex", "托盘图标异常", "", "", "")
    return {
        "text": rows.as_text(),
        "rows": rows.as_dict(),
        "color": ERROR_COLOR,
        "active_count": 0,
        "quota_tier": "unavailable",
        "quota_state": "tray_error",
    }
