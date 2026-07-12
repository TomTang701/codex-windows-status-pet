"""Trace one long-lived production-equivalent Pet across runtime transitions."""

from __future__ import annotations

import ctypes
import gc
import inspect
import json
import runpy
import sys
import tempfile
import tkinter as tk
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from api.display_api import dpi_for_window, monitor_snapshot
from api.runtime_api import enable_dpi_awareness


ROWS = {
    "activity": "Codex 空闲",
    "progress": "没有活动中的对话",
    "primary_5h": "5h 0% / 19:00",
    "weekly": "周 36% / 23:17 7/17",
    "reset_credit": "重置 5 次 / 21:09 7/11",
}

CONFIG = {
    "schema_version": 1,
    "alpha": 0.35,
    "font_color": "#e5e7eb",
    "font_size": 8,
    "background_color": "#000000",
    "topmost": True,
    "locked": False,
    "x": 4150,
    "y": 1246,
    "window_width": 264,
    "window_height": 110,
    "scale_mode": "proportional",
    "window_scale_percent": 80,
    "refresh_interval_seconds": 5,
    "compact_when_idle": False,
}


class DummyProc:
    def poll(self):
        return None


class DummyServer:
    def __init__(self, _queue):
        self.proc = DummyProc()

    def start(self):
        self.proc = DummyProc()

    def read_limits(self):
        return {"rateLimits": {"primary": {"usedPercent": 0}}}

    def stop(self):
        self.proc = None


class DummyTray:
    def __init__(self, _actions):
        pass

    def stop(self):
        pass


def _json_value(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    return str(value)


def _pack_info(widget):
    try:
        return {key: _json_value(value) for key, value in widget.pack_info().items()}
    except tk.TclError:
        return None


def _client_size(hwnd):
    rect = (ctypes.c_long * 4)()
    if not ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect)):
        return None
    return [rect[2] - rect[0], rect[3] - rect[1]]


def _shell_identity(widget_hwnd):
    user32 = ctypes.windll.user32
    root = user32.GetAncestor(widget_hwnd, 2)
    style = int(user32.GetWindowLongPtrW(root, -20)) & 0xFFFFFFFF
    return {
        "root_hwnd": int(root),
        "toolwindow": bool(style & 0x00000080),
        "appwindow": bool(style & 0x00040000),
    }


def _monitor_for(app):
    x, y = app.winfo_rootx(), app.winfo_rooty()
    for monitor in monitor_snapshot():
        left, top, right, bottom = monitor["rect"]
        if left <= x < right and top <= y < bottom:
            return monitor
    return None


def capture(app, transition, stage):
    labels = []
    root_top = app.winfo_rooty()
    root_bottom = root_top + app.winfo_height()
    text_top = app.text.winfo_rooty()
    text_bottom = text_top + app.text.winfo_height()
    for name, label in app.text.labels.items():
        top = label.winfo_rooty()
        bottom = top + label.winfo_height()
        labels.append(
            {
                "name": name,
                "text": label.cget("text"),
                "x": label.winfo_x(),
                "y": label.winfo_y(),
                "width": label.winfo_width(),
                "height": label.winfo_height(),
                "reqwidth": label.winfo_reqwidth(),
                "reqheight": label.winfo_reqheight(),
                "root_top": top,
                "root_bottom": bottom,
                "inside_root": top >= root_top and bottom <= root_bottom,
                "inside_status": top >= text_top and bottom <= text_bottom,
                "height_fits": label.winfo_reqheight() <= label.winfo_height(),
                "single_line_fits": label.winfo_reqwidth() <= label.winfo_width(),
            }
        )
    hwnd = app.winfo_id()
    shell_identity = _shell_identity(hwnd)
    final = labels[-1]
    fit = (
        len(labels) == 5
        and app.winfo_reqheight() <= app.winfo_height()
        and app.text.winfo_reqheight() <= app.text.winfo_height()
        and all(
            row["inside_root"]
            and row["inside_status"]
            and row["height_fits"]
            and row["single_line_fits"]
            for row in labels
        )
        and final["root_bottom"] <= root_bottom
    )
    return {
        "transition": transition,
        "stage": stage,
        "logical_scale": app.settings["window_scale_percent"],
        "compatibility_geometry": [app.settings["window_width"], app.settings["window_height"]],
        "position": [app.winfo_rootx(), app.winfo_rooty()],
        "monitor": _monitor_for(app),
        "dpi": dpi_for_window(hwnd),
        "tk_scaling": float(app.tk.call("tk", "scaling")),
        "window_metrics": asdict(app.window_metrics),
        "geometry": app.geometry(),
        "root_actual": [app.winfo_width(), app.winfo_height()],
        "root_requested": [app.winfo_reqwidth(), app.winfo_reqheight()],
        "client_size": _client_size(hwnd),
        "shell_identity": shell_identity,
        "battery_pack": _pack_info(app.battery),
        "text_pack": _pack_info(app.text),
        "status_actual": [app.text.winfo_width(), app.text.winfo_height()],
        "status_requested": [app.text.winfo_reqwidth(), app.text.winfo_reqheight()],
        "status_root_bounds": [text_top, text_bottom],
        "root_visible_bounds": [root_top, root_bottom],
        "labels": labels,
        "final_row_bottom": final["root_bottom"],
        "visible_root_bottom": root_bottom,
        "fits": fit,
    }


def find_widget(root, widget_type, text):
    queue = [root]
    while queue:
        widget = queue.pop(0)
        if isinstance(widget, widget_type) and str(widget.cget("text")) == text:
            return widget
        queue.extend(widget.winfo_children())
    raise LookupError(text)


def find_scales(root):
    result = []
    queue = [root]
    while queue:
        widget = queue.pop(0)
        if isinstance(widget, tk.Scale):
            result.append(widget)
        queue.extend(widget.winfo_children())
    return result


def settle(app, records, transition):
    records.append(capture(app, transition, "before_update_idletasks"))
    app.update_idletasks()
    records.append(capture(app, transition, "after_update_idletasks"))
    app.update()
    records.append(capture(app, transition, "after_update"))


def close_dialog(app):
    if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
        find_widget(app.settings_dialog, tk.Button, "Close").invoke()
        app.update_idletasks()
        app.update()


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
    enable_dpi_awareness()
    geometry_calls = []
    transition = {"name": "cold_start"}
    original_geometry = tk.Wm.geometry

    def traced_geometry(widget, new_geometry=None):
        if new_geometry is not None:
            caller = inspect.stack()[1]
            metrics = getattr(widget, "window_metrics", None)
            geometry_calls.append(
                {
                    "transition": transition["name"],
                    "requested": str(new_geometry),
                    "caller": f"{caller.function}:{caller.lineno}",
                    "dpi_before": dpi_for_window(widget.winfo_id()),
                    "position_before": [widget.winfo_rootx(), widget.winfo_rooty()],
                    "actual_before": [widget.winfo_width(), widget.winfo_height()],
                    "metrics": asdict(metrics) if metrics is not None else None,
                }
            )
        return original_geometry(widget, new_geometry)

    tk.Wm.geometry = traced_geometry
    with tempfile.TemporaryDirectory() as directory:
        home = Path(directory)
        config_path = home / ".codex" / "codex-windows-status-pet.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps(CONFIG), encoding="utf-8")
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

                transition["name"] = "toggle_locked_only"
                app.locked_var.set(not app.locked_var.get())
                app.toggle_locked()
                settle(app, records, transition["name"])

                transition["name"] = "open_settings_only"
                app.show_settings()
                settle(app, records, transition["name"])

                transition["name"] = "settings_close_without_changes"
                close_dialog(app)
                settle(app, records, transition["name"])

                transition["name"] = "opacity_only_apply"
                app.show_settings()
                scales = find_scales(app.settings_dialog)
                scales[0].set(0.45)
                find_widget(app.settings_dialog, tk.Button, "Apply").invoke()
                settle(app, records, transition["name"])
                close_dialog(app)

                transition["name"] = "scale_change_apply"
                app.show_settings()
                scales = find_scales(app.settings_dialog)
                scales[1].set(100)
                find_widget(app.settings_dialog, tk.Button, "Apply").invoke()
                settle(app, records, transition["name"])

                transition["name"] = "save"
                find_widget(app.settings_dialog, tk.Button, "Save").invoke()
                settle(app, records, transition["name"])

                transition["name"] = "draft_scale_close_rollback"
                app.show_settings()
                find_scales(app.settings_dialog)[1].set(150)
                close_dialog(app)
                settle(app, records, transition["name"])

                transition["name"] = "restore_defaults"
                app.show_settings()
                find_widget(app.settings_dialog, tk.Button, "Restore Defaults").invoke()
                find_widget(app.settings_dialog, tk.Button, "Apply").invoke()
                settle(app, records, transition["name"])
                close_dialog(app)

                for index in range(3):
                    transition["name"] = f"repeated_settings_{index + 1}"
                    app.show_settings()
                    close_dialog(app)
                    settle(app, records, transition["name"])

                transition["name"] = "hide_show"
                app.hide_window()
                app.show_window()
                settle(app, records, transition["name"])

                transition["name"] = "compact_expand"
                app.set_compact(True)
                app.set_compact(False)
                settle(app, records, transition["name"])

                transition["name"] = "combined_lock_settings_apply_close_hide_show"
                app.locked_var.set(not app.locked_var.get())
                app.toggle_locked()
                app.show_settings()
                find_scales(app.settings_dialog)[0].set(0.55)
                find_widget(app.settings_dialog, tk.Button, "Apply").invoke()
                close_dialog(app)
                app.hide_window()
                app.show_window()
                settle(app, records, transition["name"])
            finally:
                destroy_app(app)
        finally:
            Path.home = original_home
            tk.Wm.geometry = original_geometry

    output = {
        "source_version": module["APP_VERSION"],
        "geometry_calls": geometry_calls,
        "records": records,
    }
    output_path = ROOT / ".build" / "v051-runtime-transition-probe.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = []
    for name in dict.fromkeys(item["transition"] for item in records):
        after = next(
            item for item in reversed(records)
            if item["transition"] == name and item["stage"] == "after_update"
        )
        summary.append(
            {
                "transition": name,
                "scale": after["logical_scale"],
                "dpi": after["dpi"],
                "tk_scaling": after["tk_scaling"],
                "metrics": [after["window_metrics"]["width"], after["window_metrics"]["height"]],
                "actual": after["root_actual"],
                "requested": after["root_requested"],
                "final_height": [after["labels"][-1]["height"], after["labels"][-1]["reqheight"]],
                "fits": after["fits"],
            }
        )
    print(json.dumps({"artifact": str(output_path), "summary": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
