"""Small idempotent lifecycle state machine independent from Tk."""

from __future__ import annotations


class WindowLifecycleController:
    def __init__(self):
        self.closing = False

    def begin_close(self) -> bool:
        if self.closing:
            return False
        self.closing = True
        return True
