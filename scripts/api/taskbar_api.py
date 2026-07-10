"""Windows taskbar edge/rectangle diagnostics for compatibility evidence."""

from __future__ import annotations

import ctypes
from ctypes import wintypes


TASKBAR_EDGES = {0: "left", 1: "top", 2: "right", 3: "bottom"}


def edge_name(edge):
    return TASKBAR_EDGES.get(int(edge), "unknown")


def taskbar_snapshot():
    """Return the primary taskbar edge and rectangle, or an unavailable result."""
    try:
        shell = ctypes.windll.shell32
    except AttributeError:
        return {"available": False, "edge": "unknown", "rect": None}

    class Rect(ctypes.Structure):
        _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG), ("right", wintypes.LONG), ("bottom", wintypes.LONG)]

    class AppBarData(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD), ("hWnd", wintypes.HWND),
            ("uCallbackMessage", wintypes.UINT), ("uEdge", wintypes.UINT),
            ("rc", Rect), ("lParam", wintypes.LPARAM),
        ]

    data = AppBarData()
    data.cbSize = ctypes.sizeof(AppBarData)
    try:
        result = shell.SHAppBarMessage(5, ctypes.byref(data))
    except (AttributeError, OSError):
        return {"available": False, "edge": "unknown", "rect": None}
    if not result:
        return {"available": False, "edge": "unknown", "rect": None}
    return {
        "available": True,
        "edge": edge_name(data.uEdge),
        "rect": [data.rc.left, data.rc.top, data.rc.right, data.rc.bottom],
    }
