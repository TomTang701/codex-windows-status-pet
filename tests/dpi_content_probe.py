"""Isolated production-order DPI/Tk content-fit probe used by regression tests."""

from __future__ import annotations

import gc
import json
import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from api.runtime_api import enable_dpi_awareness


enable_dpi_awareness()

from api.display_api import dpi_for_window


class DummyServer:
    def __init__(self, _queue):
        self.proc = None

    def stop(self):
        pass


class DummyTray:
    def __init__(self, _actions):
        pass

    def stop(self):
        pass


ROWS = {
    "activity": "Codex 空闲",
    "progress": "没有活动中的对话",
    "primary_5h": "5h 0% / 14:00",
    "weekly": "周 57% / 23:17 7/17",
    "reset_credit": "重置 5 次 / 18:40 7/12",
}


def destroy_app(app):
    app.application_controller.shutdown()
    for callback in app.tk.call("after", "info"):
        try:
            app.after_cancel(callback)
        except Exception:
            pass
    app.topmost_var = None
    app.locked_var = None
    app.destroy()
    gc.collect()


def main():
    module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
    module["AppServer"] = DummyServer
    module["TrayIcon3"] = DummyTray
    results = []
    effective_dpi = None
    for scale in range(80, 201, 5):
        app = module["Pet"]()
        try:
            app.apply_settings(
                {**app.settings, "window_scale_percent": scale, "x": 100, "y": 100}
            )
            app.text.configure_rows(rows=ROWS)
            app.update()
            effective_dpi = dpi_for_window(app.winfo_id())
            labels = list(app.text.labels.values())
            reset = app.text.labels["reset_credit"]
            cells = list(app.battery.cells)
            fits = (
                app.winfo_reqheight() <= app.winfo_height()
                and app.text.winfo_reqheight() <= app.text.winfo_height()
                and all(
                    label.winfo_reqheight() <= label.winfo_height()
                    and label.winfo_y() + label.winfo_height()
                    <= app.text.winfo_height()
                    for label in labels
                )
                and reset.winfo_reqwidth() <= reset.winfo_width()
                and len(cells) == 10
                and all(
                    cell.winfo_ismapped()
                    and cell.winfo_x() >= 0
                    and cell.winfo_y() >= 0
                    and cell.winfo_x() + cell.winfo_width() <= app.winfo_width()
                    and cell.winfo_y() + cell.winfo_height() <= app.winfo_height()
                    for cell in cells
                )
            )
            results.append(
                {
                    "scale": scale,
                    "root_actual": [app.winfo_width(), app.winfo_height()],
                    "root_requested": [app.winfo_reqwidth(), app.winfo_reqheight()],
                    "status_actual": [
                        app.text.winfo_width(),
                        app.text.winfo_height(),
                    ],
                    "status_requested": [
                        app.text.winfo_reqwidth(),
                        app.text.winfo_reqheight(),
                    ],
                    "reset_actual": [reset.winfo_width(), reset.winfo_height()],
                    "reset_requested": [
                        reset.winfo_reqwidth(),
                        reset.winfo_reqheight(),
                    ],
                    "row_count": len(labels),
                    "battery_cells": len(cells),
                    "fits": fits,
                }
            )
        finally:
            destroy_app(app)
    output = {
        "dpi": effective_dpi,
        "all_fit": all(item["fits"] for item in results),
        "rows": results,
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0 if output["all_fit"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
