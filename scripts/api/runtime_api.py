"""Runtime lifecycle API for safe single-instance ownership."""

from __future__ import annotations

import ctypes


def enable_dpi_awareness():
    """Ask Windows for per-monitor coordinates before creating Tk windows."""
    try:
        result = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return result in (0, 0x80070005)
    except (AttributeError, OSError):
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
