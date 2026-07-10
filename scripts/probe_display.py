"""Print a display/DPI diagnostic snapshot for mixed-DPI troubleshooting."""

from __future__ import annotations

import json
import ctypes
from pathlib import Path

from api.display_api import dpi_for_window, monitor_snapshot, virtual_desktop_bounds
from api.taskbar_api import taskbar_snapshot


def main():
    hwnd = ctypes.windll.user32.FindWindowW(None, "Codex Windows Status Pet")
    result = {
        "virtual_desktop": virtual_desktop_bounds(),
        "monitors": monitor_snapshot(),
        "overlay_window": {"hwnd": int(hwnd), "dpi": dpi_for_window(hwnd)} if hwnd else None,
        "config_path": str(Path.home() / ".codex" / "codex-windows-status-pet.json"),
        "taskbar": taskbar_snapshot(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
