"""Normalize local provider responses without owning network or auth state."""

from __future__ import annotations


def normalize_snapshot(payload):
    """Return a stable local snapshot shape from an app-server response.

    This API deliberately accepts already-fetched data only. It never reads
    auth files, creates HTTP clients, or stores credentials.
    """
    if not isinstance(payload, dict):
        return {"status": "unavailable", "rateLimits": {}, "rateLimitResetCredits": {}}
    limits = payload.get("rateLimits")
    credits = payload.get("rateLimitResetCredits")
    return {
        "status": "available" if isinstance(limits, dict) else "unavailable",
        "rateLimits": limits if isinstance(limits, dict) else {},
        "rateLimitResetCredits": credits if isinstance(credits, (dict, list)) else {},
    }
