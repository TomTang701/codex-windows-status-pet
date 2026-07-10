"""Normalize local provider responses without owning network or auth state."""

from __future__ import annotations

from .quota_parse_api import parse_quota_payload


def normalize_snapshot(payload):
    """Return a stable local snapshot shape from an app-server response.

    This API deliberately accepts already-fetched data only. It never reads
    auth files, creates HTTP clients, or stores credentials.
    """
    return parse_quota_payload(payload)
