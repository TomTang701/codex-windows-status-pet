"""Compact geometry helpers."""

from __future__ import annotations


def compact_geometry(x, y, expanded_width, expanded_height, compact_size, work_area, margin=8):
    """Keep the compact orb anchored to the right/bottom edge when applicable."""
    left, top, right, bottom = work_area
    x = int(x)
    y = int(y)
    size = int(compact_size)
    if x + int(expanded_width) >= right - margin:
        x = x + int(expanded_width) - size
    if y + int(expanded_height) >= bottom - margin:
        y = y + int(expanded_height) - size
    return min(max(x, left), max(left, right - size)), min(max(y, top), max(top, bottom - size))
