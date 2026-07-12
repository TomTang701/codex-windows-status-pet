"""Test target-window DPI/Tk-scaling synchronization without production edits."""

from __future__ import annotations

import json
import runpy
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from api.display_api import dpi_for_window
from api.runtime_api import enable_dpi_awareness
from runtime_geometry_transition_probe import (
    CONFIG,
    DummyServer,
    DummyTray,
    ROWS,
    destroy_app,
    settle,
)


def summary(records, transition):
    item = next(
        record
        for record in reversed(records)
        if record["transition"] == transition and record["stage"] == "after_update"
    )
    return {
        "transition": transition,
        "scale": item["logical_scale"],
        "dpi": item["dpi"],
        "tk_scaling": item["tk_scaling"],
        "metrics": [item["window_metrics"]["width"], item["window_metrics"]["height"]],
        "actual": item["root_actual"],
        "requested": item["root_requested"],
        "final_height": [item["labels"][-1]["height"], item["labels"][-1]["reqheight"]],
        "fits": item["fits"],
    }


def main():
    enable_dpi_awareness()
    with tempfile.TemporaryDirectory() as directory:
        home = Path(directory)
        path = home / ".codex" / "codex-windows-status-pet.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(CONFIG), encoding="utf-8")
        original_home = Path.home
        Path.home = classmethod(lambda cls: home)
        try:
            module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
            module["AppServer"] = DummyServer
            module["TrayIcon3"] = DummyTray
            app = module["Pet"]()
            records = []
            try:
                app.text.configure_rows(rows=ROWS)
                settle(app, records, "cold_start")

                target_dpi = dpi_for_window(app.winfo_id())
                app.tk.call("tk", "scaling", target_dpi / 72.0)
                app.apply_settings(app.settings)
                settle(app, records, "target_dpi_baseline")

                metrics = app.window_metrics
                app.battery.set_metrics(metrics.text_font_size)
                app.text.configure_rows(
                    font=("Segoe UI", -round(metrics.text_font_size * target_dpi / 72.0)),
                    wraplength=metrics.wraplength,
                )
                settle(app, records, "target_dpi_pixel_fonts")

                app.locked_var.set(not app.locked_var.get())
                app.toggle_locked()
                settle(app, records, "toggle_after_target_dpi_baseline")
            finally:
                destroy_app(app)
        finally:
            Path.home = original_home
    print(
        json.dumps(
            {
                "cold": summary(records, "cold_start"),
                "target_dpi_baseline": summary(records, "target_dpi_baseline"),
                "target_dpi_pixel_fonts": summary(records, "target_dpi_pixel_fonts"),
                "toggle_after_baseline": summary(records, "toggle_after_target_dpi_baseline"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
