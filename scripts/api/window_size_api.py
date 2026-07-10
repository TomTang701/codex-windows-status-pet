"""Pure window-size transformations for the settings UI."""

from __future__ import annotations


def resize_dimensions(width, height, factor, proportional=False,
                      width_bounds=(180, 1200), height_bounds=(80, 800)):
    """Return bounded dimensions after a plus/minus resize operation."""
    try:
        width = int(width)
        height = int(height)
        factor = float(factor)
    except (TypeError, ValueError):
        raise ValueError("width, height, and factor must be numeric")
    if factor <= 0:
        raise ValueError("factor must be positive")
    next_width = round(width * factor)
    next_height = round(height * factor) if proportional else height
    return (
        min(width_bounds[1], max(width_bounds[0], next_width)),
        min(height_bounds[1], max(height_bounds[0], next_height)),
    )
