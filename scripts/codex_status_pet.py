"""Stable launcher facade for the modular Windows status-pet application."""

from __future__ import annotations

try:
    from scripts.ui import main_window as _main_window
except ModuleNotFoundError:
    from ui import main_window as _main_window


# Preserve the historical import surface for tests and integrations while the
# implementation lives in the UI adapter module.
AppServer = _main_window.AppServer
TrayIcon3 = _main_window.TrayIcon3
ActivityMonitor = _main_window.ActivityMonitor
ensure_single_instance = _main_window.ensure_single_instance
enable_dpi_awareness = _main_window.enable_dpi_awareness
configure_logging = _main_window.configure_logging


class Pet(_main_window.Pet):
    """Compatibility facade that keeps injectable test dependencies working."""

    def __init__(self, *args, **kwargs):
        _main_window.AppServer = AppServer
        _main_window.TrayIcon3 = TrayIcon3
        super().__init__(*args, **kwargs)


def run():
    """Delegate production startup to the modular main-window implementation."""
    return _main_window.run()


if __name__ == "__main__":
    run()
