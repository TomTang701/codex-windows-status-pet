"""Runtime lifecycle API for safe single-instance ownership."""

from __future__ import annotations

import ctypes


GWL_EXSTYLE = -20
GA_ROOT = 2
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_FRAMECHANGED = 0x0020


def enable_dpi_awareness():
    """Ask Windows for per-monitor coordinates before creating Tk windows."""
    try:
        result = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return result in (0, 0x80070005)
    except (AttributeError, OSError):
        return False


def ensure_overlay_toolwindow(widget_hwnd):
    """Keep the real Tk top-level window out of ordinary Shell switchers."""
    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.GetAncestor.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        user32.GetAncestor.restype = ctypes.c_void_p
        user32.GetWindowLongPtrW.argtypes = (ctypes.c_void_p, ctypes.c_int)
        user32.GetWindowLongPtrW.restype = ctypes.c_ssize_t
        user32.SetWindowLongPtrW.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_ssize_t)
        user32.SetWindowLongPtrW.restype = ctypes.c_ssize_t
        user32.SetWindowPos.argtypes = (
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_uint,
        )
        user32.SetWindowPos.restype = ctypes.c_bool

        root = user32.GetAncestor(ctypes.c_void_p(widget_hwnd), GA_ROOT)
        if not root:
            return False
        current = int(user32.GetWindowLongPtrW(root, GWL_EXSTYLE)) & 0xFFFFFFFF
        target = (current | WS_EX_TOOLWINDOW) & ~WS_EX_APPWINDOW
        if target != current:
            user32.SetWindowLongPtrW(root, GWL_EXSTYLE, ctypes.c_ssize_t(target))
            user32.SetWindowPos(
                root,
                None,
                0,
                0,
                0,
                0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED,
            )
        effective = int(user32.GetWindowLongPtrW(root, GWL_EXSTYLE)) & 0xFFFFFFFF
        return bool(effective & WS_EX_TOOLWINDOW) and not bool(effective & WS_EX_APPWINDOW)
    except (AttributeError, OSError, TypeError):
        return False


class SingleInstance:
    def __init__(self, name="Local\\CodexWindowsStatusPet"):
        self.name = name
        self.handle = None

    def acquire(self):
        kernel32 = ctypes.windll.kernel32
        self.handle = kernel32.CreateMutexW(None, True, self.name)
        if not self.handle:
            return False
        if kernel32.GetLastError() == 183:
            kernel32.CloseHandle(self.handle)
            self.handle = None
            return False
        return True

    def release(self):
        if self.handle:
            ctypes.windll.kernel32.CloseHandle(self.handle)
            self.handle = None
