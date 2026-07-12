"""Pure state decisions for the optional compact/expanded overlay mode."""

from __future__ import annotations

def compact_size(width, height, minimum=64):
    """Return a square compact size while respecting the configured minimum."""
    try:
        configured = min(int(width), int(height))
    except (TypeError, ValueError):
        configured = minimum
    return max(minimum, configured // 2)
