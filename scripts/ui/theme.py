"""Shared visual language for the Signal HUD and Native Codex settings surfaces."""

from __future__ import annotations


# Microsoft YaHei UI provides stable CJK glyphs on supported Windows hosts while
# retaining the same compact, modern proportions for the English interface.
FONT_FAMILY = "Microsoft YaHei UI"

COLORS = {
    "background": "#0b1220",
    "surface": "#111827",
    "surface_alt": "#172033",
    "border": "#26354d",
    "text": "#e5e7eb",
    "muted": "#94a3b8",
    "accent": "#22d3ee",
    "accent_alt": "#818cf8",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "danger": "#f87171",
}


def scaled_font(size, weight="normal"):
    """Return a consistent bilingual font tuple for Tk widgets."""
    return (FONT_FAMILY, size, weight)
