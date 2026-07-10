"""Recover an overlay only when its saved rectangle is not on any work area."""

from __future__ import annotations


def _work_areas(monitors):
    return [tuple(monitor["work"]) for monitor in (monitors or []) if isinstance(monitor, dict) and len(monitor.get("work", ())) == 4]


def rectangle_intersects_work_area(x, y, width, height, work):
    left, top, right, bottom = work
    return x < right and x + width > left and y < bottom and y + height > top


def _distance_to_work_area(x, y, work):
    left, top, right, bottom = work
    dx = max(left - x, 0, x - right)
    dy = max(top - y, 0, y - bottom)
    return dx * dx + dy * dy


def recover_position(x, y, width, height, monitors, fallback=(0, 0, 1920, 1080)):
    """Keep legal multi-monitor coordinates, otherwise clamp to nearest work area."""
    areas = _work_areas(monitors)
    if not areas:
        areas = [tuple(fallback)]
    if any(rectangle_intersects_work_area(x, y, width, height, area) for area in areas):
        return int(x), int(y), False
    area = min(areas, key=lambda candidate: _distance_to_work_area(x, y, candidate))
    left, top, right, bottom = area
    recovered_x = min(max(int(x), left), max(left, right - int(width)))
    recovered_y = min(max(int(y), top), max(top, bottom - int(height)))
    return recovered_x, recovered_y, True
