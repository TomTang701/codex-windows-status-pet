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
    if isinstance(used, (int, float)) and not isinstance(used, bool):
        result["usedPercent"] = used
    if isinstance(reset, (int, float, str)) and not isinstance(reset, bool):
        result["resetsAt"] = reset
    return result


def parse_quota_payload(payload):
    if not isinstance(payload, dict):
        return {"status": "unavailable", "rateLimits": {}, "rateLimitResetCredits": {}}
    limits = _first(payload, "rateLimits", "rate_limits")
    parsed_limits = {}
    if isinstance(limits, dict):
        for source, target in (("primary", "primary"), ("secondary", "secondary"), ("weekly", "secondary")):
            if target not in parsed_limits:
                window = _window(_first(limits, source))
                if window:
                    parsed_limits[target] = window
    credits = _first(payload, "rateLimitResetCredits", "rate_limit_reset_credits")
    parsed_credits = {}
    if isinstance(credits, dict):
        count = _first(credits, "availableCount", "available_count")
        if isinstance(count, int) and not isinstance(count, bool):
            parsed_credits["availableCount"] = count
        expirations = _first(credits, "resetsAt", "resetAt", "expirations")
        if isinstance(expirations, list):
            parsed_credits["resetsAt"] = [item for item in expirations if isinstance(item, (int, float, str)) and not isinstance(item, bool)]
        elif isinstance(expirations, (int, float, str)) and not isinstance(expirations, bool):
            parsed_credits["resetsAt"] = [expirations]
    return {
        "status": "available" if parsed_limits else "unavailable",
        "rateLimits": parsed_limits,
        "rateLimitResetCredits": parsed_credits,
    }
