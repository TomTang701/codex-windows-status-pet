"""Check whether a withdrawn Tk root acquires target-monitor DPI after positioning."""

from __future__ import annotations

import json
import sys
import tkinter as tk
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from api.display_api import dpi_for_window
from api.runtime_api import enable_dpi_awareness


enable_dpi_awareness()
root = tk.Tk()
try:
    initial = dpi_for_window(root.winfo_id())
    root.withdraw()
    root.geometry("+4150+1246")
    before_update = dpi_for_window(root.winfo_id())
    root.update_idletasks()
    after_idle = dpi_for_window(root.winfo_id())
    withdrawn_position = [root.winfo_rootx(), root.winfo_rooty()]
    root.deiconify()
    root.update_idletasks()
    after_deiconify = dpi_for_window(root.winfo_id())
    print(
        json.dumps(
            {
                "initial": initial,
                "before_update": before_update,
                "after_idle_withdrawn": after_idle,
                "withdrawn_position": withdrawn_position,
                "after_deiconify": after_deiconify,
                "mapped": bool(root.winfo_ismapped()),
            },
            indent=2,
        )
    )
finally:
    root.destroy()
