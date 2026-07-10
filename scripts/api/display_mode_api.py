"""Pure state decisions for the optional compact/expanded overlay mode."""

from __future__ import annotations


def should_compact(enabled, active_count, hovered=False):
    """Compact only when explicitly enabled, idle, and not under the pointer."""
    return bool(enabled) and int(active_count or 0) == 0 and not hovered


def compact_size(width, height, minimum=64):
    """Return a square compact size while respecting the configured minimum."""
    try:
        configured = min(int(width), int(height))
    except (TypeError, ValueError):
        configured = minimum
    return max(minimum, configured // 2)
