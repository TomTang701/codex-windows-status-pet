"""Recover an overlay only when its saved rectangle is not on any work area."""

from __future__ import annotations


def _work_areas(monitors):
    return [tuple(monitor["work"]) for monitor in (monitors or []) if isinstance(monitor, dict) and len(monitor.get("work", ())) == 4]


def rectangle_intersects_work_area(x, y, width, height, work):
    left, top, right, bottom = work
    return x < right and x + width > left and y < bottom and y + height > top


def rectangle_contained_in_work_area(x, y, width, height, work, edge_tolerance=8):
    """Return True when a window is contained, allowing tiny DPI rounding overflow."""
    left, top, right, bottom = work
    tolerance = max(0, int(edge_tolerance))
    return x >= left - tolerance and y >= top - tolerance and x + width <= right + tolerance and y + height <= bottom + tolerance


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
    if any(rectangle_contained_in_work_area(x, y, width, height, area) for area in areas):
        return int(x), int(y), False
    intersecting = [area for area in areas if rectangle_intersects_work_area(x, y, width, height, area)]
    if intersecting:
        def overlap_area(area):
            left, top, right, bottom = area
            overlap_width = max(0, min(x + width, right) - max(x, left))
            overlap_height = max(0, min(y + height, bottom) - max(y, top))
            return overlap_width * overlap_height

        area = max(intersecting, key=overlap_area)
    else:
        area = min(areas, key=lambda candidate: _distance_to_work_area(x, y, candidate))
    left, top, right, bottom = area
    recovered_x = min(max(int(x), left), max(left, right - int(width)))
    recovered_y = min(max(int(y), top), max(top, bottom - int(height)))
    return recovered_x, recovered_y, True
