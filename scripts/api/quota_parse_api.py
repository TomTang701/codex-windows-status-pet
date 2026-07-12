"""Strict parser for the approved local app-server quota fields."""

from __future__ import annotations

from datetime import datetime


def _first(mapping, *names):
    if not isinstance(mapping, dict):
        return None
    for name in names:
        if name in mapping:
            return mapping[name]
    return None


def _window(value):
    if not isinstance(value, dict):
        return {}
    result = {}
    used = _first(value, "usedPercent", "used_percent")
    reset = _first(value, "resetsAt", "resets_at")
    duration = _first(value, "windowDurationMins", "window_duration_mins")
    if isinstance(used, (int, float)) and not isinstance(used, bool):
        result["usedPercent"] = used
    if isinstance(reset, (int, float, str)) and not isinstance(reset, bool):
        result["resetsAt"] = reset
    if isinstance(duration, int) and not isinstance(duration, bool):
        result["windowDurationMins"] = duration
    return result


_WINDOW_SLOT_BY_DURATION_MINUTES = {300: "primary", 10080: "secondary"}


_EXPIRY_NAMES = ("expiresAt", "expires_at", "resetsAt", "resets_at", "resetAt", "reset_at")
_EXPIRY_CONTAINERS = ("expirations", "credits")


def _approved_expirations(value, depth=0):
    """Extract approved Reset Credit expiry fields without traversing arbitrary payload data."""
    if depth > 3:
        return []
    if isinstance(value, (int, float, str)) and not isinstance(value, bool):
        return [value]
    if isinstance(value, (list, tuple)):
        result = []
        for item in value:
            result.extend(_approved_expirations(item, depth + 1))
        return result
    if not isinstance(value, dict):
        return []
    result = []
    for name in _EXPIRY_NAMES:
        if name in value:
            result.extend(_approved_expirations(value[name], depth + 1))
    for name in _EXPIRY_CONTAINERS:
        if name in value:
            result.extend(_approved_expirations(value[name], depth + 1))
    return result


def parse_quota_payload(payload):
    if not isinstance(payload, dict):
        return {"status": "unavailable", "rateLimits": {}, "rateLimitResetCredits": {}}
    limits = _first(payload, "rateLimits", "rate_limits")
    parsed_limits = {}
    if isinstance(limits, dict):
        for value in limits.values():
            window = _window(value)
            target = _WINDOW_SLOT_BY_DURATION_MINUTES.get(window.get("windowDurationMins"))
            if target and target not in parsed_limits:
                parsed_limits[target] = window
    credits = _first(payload, "rateLimitResetCredits", "rate_limit_reset_credits")
    parsed_credits = {}
    if isinstance(credits, dict):
        count = _first(credits, "availableCount", "available_count")
        if isinstance(count, int) and not isinstance(count, bool):
            parsed_credits["availableCount"] = count
        expirations = _approved_expirations(credits)
        if expirations:
            parsed_credits["resetsAt"] = expirations
    return {
        "status": "available" if parsed_limits else "unavailable",
        "rateLimits": parsed_limits,
        "rateLimitResetCredits": parsed_credits,
    }
