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
