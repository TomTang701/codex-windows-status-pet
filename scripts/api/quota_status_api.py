"""Pure quota health classification for the overlay presentation layer."""

from __future__ import annotations


def remaining_percent(window):
    if not isinstance(window, dict):
        return None
    try:
        used = float(window.get("usedPercent"))
    except (TypeError, ValueError):
        return None
    return max(0.0, min(100.0, 100.0 - used))


def health_tier(window):
    remaining = remaining_percent(window)
    if remaining is None:
        return "unavailable"
    if remaining >= 50:
        return "healthy"
    if remaining >= 10:
        return "caution"
    return "critical"


HEALTH_COLORS = {
    "healthy": "#e5e7eb",
    "caution": "#fbbf24",
    "critical": "#f87171",
    "unavailable": "#fca5a5",
}
