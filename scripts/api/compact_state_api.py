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


def canonical_expanded_position(
    compact_x,
    compact_y,
    expanded_width,
    expanded_height,
    compact_size,
    work_area,
    margin=8,
):
    """Convert a derived compact visible position back to canonical expanded coordinates."""
    left, top, right, bottom = work_area
    compact_x = int(compact_x)
    compact_y = int(compact_y)
    expanded_width = int(expanded_width)
    expanded_height = int(expanded_height)
    compact_size = int(compact_size)
    margin = max(0, int(margin))
    if compact_x >= right - compact_size - margin:
        compact_x -= expanded_width - compact_size
    if compact_y >= bottom - compact_size - margin:
        compact_y -= expanded_height - compact_size
    return compact_x, compact_y
