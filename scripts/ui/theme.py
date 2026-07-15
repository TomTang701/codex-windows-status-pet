"""Shared visual language for the Signal HUD and Native Codex settings surfaces."""

from __future__ import annotations


FONT_FAMILY = "Segoe UI"

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
    """Return a consistent Segoe UI tuple for Tk widgets."""
    return (FONT_FAMILY, size, weight)
