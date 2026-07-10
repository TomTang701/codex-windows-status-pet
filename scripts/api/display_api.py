"""Display and DPI API for multi-monitor diagnostics and geometry tests."""

from __future__ import annotations

import ctypes


def virtual_desktop_bounds():
    """Return the Windows virtual desktop as (left, top, width, height)."""
    try:
        user32 = ctypes.windll.user32
        return (
            user32.GetSystemMetrics(76),
            user32.GetSystemMetrics(77),
            user32.GetSystemMetrics(78),
            user32.GetSystemMetrics(79),
        )
    except (AttributeError, OSError):
        return None


def dpi_for_window(hwnd):
    """Return a window's effective DPI, or 96 when Windows cannot provide it."""
    try:
        dpi = int(ctypes.windll.user32.GetDpiForWindow(hwnd))
        return dpi or 96
    except (AttributeError, OSError, TypeError, ValueError):
        return 96


def scale_for_dpi(dpi):
    try:
        return max(0.5, float(dpi) / 96.0)
    except (TypeError, ValueError):
        return 1.0


def rectangle_intersects_virtual_desktop(x, y, width, height, bounds):
    """Check visibility without clamping intentional multi-monitor coordinates."""
    if not bounds:
        return True
    left, top, desktop_width, desktop_height = bounds
    right = left + desktop_width
    bottom = top + desktop_height
    return x < right and x + width > left and y < bottom and y + height > top
