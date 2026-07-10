"""Runtime lifecycle API for safe single-instance ownership."""

from __future__ import annotations

import ctypes


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
