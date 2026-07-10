"""Display and DPI API for multi-monitor diagnostics and geometry tests."""

from __future__ import annotations

import ctypes
from ctypes import wintypes


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


def place_popup(anchor_x, anchor_y, popup_width, popup_height, work_area, margin=8):
    """Place a popup fully inside one monitor work area.

    The anchor is normally the pointer position. The algorithm prefers the
    lower-right quadrant, then flips each axis when space is unavailable, and
    finally clamps the result. All coordinates are virtual-desktop coordinates.
    """
    left, top, right, bottom = work_area
    width = max(1, int(popup_width))
    height = max(1, int(popup_height))
    margin = max(0, int(margin))
    x = anchor_x + margin
    y = anchor_y + margin
    if x + width > right - margin:
        x = anchor_x - width - margin
    if y + height > bottom - margin:
        y = anchor_y - height - margin
    max_x = max(left + margin, right - width - margin)
    max_y = max(top + margin, bottom - height - margin)
    return min(max(x, left + margin), max_x), min(max(y, top + margin), max_y)


def work_area_for_point(x, y, monitors=None):
    """Return the work rectangle containing a virtual-desktop point."""
    monitors = monitor_snapshot() if monitors is None else monitors
    for monitor in monitors:
        left, top, right, bottom = monitor.get("work", ())
        if left <= x < right and top <= y < bottom:
            return left, top, right, bottom
    if monitors:
        return tuple(monitors[0]["work"])
    bounds = virtual_desktop_bounds()
    if bounds:
        left, top, width, height = bounds
        return left, top, left + width, top + height
    return 0, 0, 1920, 1080


def monitor_snapshot():
    """Return monitor rectangles and legacy monitor DPI values for diagnostics."""
    try:
        user32 = ctypes.windll.user32
        shcore = ctypes.windll.shcore
    except AttributeError:
        return []

    class Rect(ctypes.Structure):
        _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG), ("right", wintypes.LONG), ("bottom", wintypes.LONG)]

    class MonitorInfo(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", Rect), ("rcWork", Rect), ("flags", wintypes.DWORD), ("name", wintypes.WCHAR * 32)]

    monitors = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(Rect), wintypes.LPARAM)
    def callback(handle, _dc, _rect, _data):
        info = MonitorInfo()
        info.cbSize = ctypes.sizeof(MonitorInfo)
        user32.GetMonitorInfoW(handle, ctypes.byref(info))
        dpi_x = ctypes.c_uint(96)
        dpi_y = ctypes.c_uint(96)
        try:
            shcore.GetDpiForMonitor(handle, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
        except OSError:
            pass
        monitors.append({
            "name": info.name,
            "rect": [info.rcMonitor.left, info.rcMonitor.top, info.rcMonitor.right, info.rcMonitor.bottom],
            "work": [info.rcWork.left, info.rcWork.top, info.rcWork.right, info.rcWork.bottom],
            "dpi_x": dpi_x.value,
            "dpi_y": dpi_y.value,
        })
        return True

    user32.EnumDisplayMonitors(0, 0, callback, 0)
    return monitors
