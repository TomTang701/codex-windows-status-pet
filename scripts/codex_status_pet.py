"""Windows Codex status overlay and notification-area companion."""

from __future__ import annotations

import os
import json
import logging
import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import colorchooser, messagebox
try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw
import pystray

APP_VERSION = "0.2.0"
try:
    from api.activity_api import snapshot_activity
    from api.config_api import DEFAULT_SETTINGS, load_settings as load_settings_api, save_settings_atomic
    from api.diagnostics_api import configure_logging
    from api.display_api import dpi_for_window, virtual_desktop_bounds, place_popup, work_area_for_point
    from api.quota_format_api import earliest_future_expiry, quota_line, reset_credit_line
    from api.refresh_scheduler_api import RefreshScheduler
    from api.quota_status_api import HEALTH_COLORS, health_tier
    from api.display_mode_api import compact_size, should_compact
    from api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from api.window_size_api import resize_dimensions
    from api.quota_provider_api import normalize_snapshot
    from api.runtime_api import SingleInstance, enable_dpi_awareness
except ModuleNotFoundError:
    from scripts.api.activity_api import snapshot_activity
    from scripts.api.config_api import DEFAULT_SETTINGS, load_settings as load_settings_api, save_settings_atomic
    from scripts.api.diagnostics_api import configure_logging
    from scripts.api.display_api import dpi_for_window, virtual_desktop_bounds, place_popup, work_area_for_point
    from scripts.api.quota_format_api import earliest_future_expiry, quota_line, reset_credit_line
    from scripts.api.refresh_scheduler_api import RefreshScheduler
    from scripts.api.quota_status_api import HEALTH_COLORS, health_tier
    from scripts.api.display_mode_api import compact_size, should_compact
    from scripts.api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from scripts.api.window_size_api import resize_dimensions
    from scripts.api.quota_provider_api import normalize_snapshot
    from scripts.api.runtime_api import SingleInstance, enable_dpi_awareness


def ensure_single_instance():
    """Claim the mutex without killing an existing process."""
    global _single_instance_guard
    _single_instance_guard = SingleInstance()
    return _single_instance_guard.acquire()


def find_codex() -> str:
    candidates = []
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured:
        candidates.append(configured)
    config = Path.home() / ".codex" / "config.toml"
    if config.exists() and tomllib:
        try:
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))

            def find_config_values(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key.lower() == "codex_cli_path" and isinstance(child, str):
                            candidates.append(child)
                        else:
                            find_config_values(child)

            find_config_values(parsed)
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            logging.getLogger("codex-status-pet").warning("unable to parse Codex config.toml", exc_info=True)
    candidates.extend(["codex.exe", "codex"])
    for candidate in candidates:
        if Path(candidate).exists():
            return str(Path(candidate))
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError("Codex CLI was not found")


class AppServer:
    def __init__(self, updates: queue.Queue):
        self.updates = updates
        self.proc = None
        self.next_id = 1
        self.pending = {}
        self.lock = threading.Lock()

    def start(self):
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = subprocess.SW_HIDE
        self.proc = subprocess.Popen(
            [find_codex(), "app-server", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            startupinfo=startup,
        )
        threading.Thread(target=self._reader, daemon=True).start()
        initialized = self._send({"method": "initialize", "params": {"clientInfo": {
            "name": "codex-windows-status-pet", "title": "Codex Windows Status Pet", "version": APP_VERSION
        }, "capabilities": {"experimentalApi": True}}})
        if "error" in initialized:
            raise RuntimeError(initialized["error"].get("message", "Codex app-server initialization failed"))
        self._send({"method": "initialized", "params": {}}, wait=False)

    def _reader(self):
        try:
            for line in self.proc.stdout:
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ident = message.get("id")
                with self.lock:
                    callback = self.pending.pop(ident, None)
                if callback:
                    callback(message)
        finally:
            self.updates.put({"error": "Codex app-server stopped"})

    def _send(self, message, wait=True):
        if not self.proc or self.proc.poll() is not None:
            raise RuntimeError("Codex app-server is not running")
        ident = None
        if wait:
            with self.lock:
                ident = self.next_id
                self.next_id += 1
                message["id"] = ident
                event = threading.Event()
                result = []
                self.pending[ident] = lambda value: (result.append(value), event.set())
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()
        if not wait:
            return None
        if not event.wait(5):
            with self.lock:
                self.pending.pop(ident, None)
            raise TimeoutError("Codex app-server request timed out")
        return result[0]

    def read_limits(self):
        response = self._send({"method": "account/rateLimits/read", "params": {}})
        if "error" in response:
            raise RuntimeError(response["error"].get("message", "rate limit request failed"))
        return response.get("result", {})

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()


def percent_left(window):
    if not isinstance(window, dict):
        return "--"
    try:
        used = int(window.get("usedPercent", 0))
    except (TypeError, ValueError):
        return "--"
    return f"{max(0, 100 - used)}%"


def short_time(epoch):
    if not epoch:
        return "--"
    try:
        return datetime.fromtimestamp(float(epoch), tz=timezone.utc).astimezone().strftime("%H:%M")
    except (TypeError, ValueError, OverflowError, OSError):
        return "--"


class ActivityMonitor:
    """Infer active turns from Codex session JSONL through the activity API."""

    def __init__(self):
        self.sessions = Path.home() / ".codex" / "sessions"
        self.stale_seconds = 600
        self.cache = {}

    def snapshot(self):
        return snapshot_activity(self.sessions, self.stale_seconds, cache=self.cache)




class TrayIcon3:
    """Stable notification-area integration backed by pystray."""

    def __init__(self, actions):
        self.actions = actions
        image = Image.new("RGBA", (64, 64), (17, 24, 39, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((12, 12, 52, 52), fill=(147, 197, 253, 255))
        draw.ellipse((22, 18, 30, 26), fill=(17, 24, 39, 255))
        draw.ellipse((34, 18, 42, 26), fill=(17, 24, 39, 255))
        menu = pystray.Menu(
            pystray.MenuItem("\u663e\u793a\u7a97\u53e3", lambda icon, item: actions.put("show")),
            pystray.MenuItem("\u9690\u85cf\u7a97\u53e3", lambda icon, item: actions.put("hide")),
            pystray.MenuItem("\u6253\u5f00\u8bbe\u7f6e", lambda icon, item: actions.put("settings")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("\u9000\u51fa", lambda icon, item: actions.put("exit")),
        )
        self.icon = pystray.Icon("codex-windows-status-pet", image, "Codex Status Pet", menu)
        self.thread = threading.Thread(target=self._run, name="codex-tray", daemon=True)
        self.thread.start()

    def _run(self):
        try:
            self.icon.run()
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon failed")
            self.actions.put("tray_error")

    def stop(self):
        try:
            self.icon.stop()
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon shutdown failed")


class Pet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Codex Windows Status Pet")
        self.overrideredirect(True)
        self.settings_path = Path.home() / ".codex" / "codex-windows-status-pet.json"
        self.closing = False
        self.settings = self.load_settings()
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.configure(bg=self.settings["background_color"])
        self.geometry(f"{self.settings['window_width']}x{self.settings['window_height']}+{self.settings['x']}+{self.settings['y']}")
        self.hidden = False
        self.hidden_position = (self.settings["x"], self.settings["y"])
        self.compact = False
        self.hovered = False
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.queue = queue.Queue()
        self.tray_actions = queue.Queue()
        self.settings_dialog = None
        self.tray_restart_scheduled = False
        self.server = AppServer(self.queue)
        self.activity = ActivityMonitor()
        self.refresh_scheduler = RefreshScheduler(self.settings["refresh_interval_seconds"])
        self.topmost_var = tk.BooleanVar(value=self.settings["topmost"])
        self.locked_var = tk.BooleanVar(value=self.settings["locked"])
        self.face = tk.Label(self, text="\U0001f43e", font=("Segoe UI Emoji", 28), fg=self.settings["font_color"], bg=self.settings["background_color"])
        self.face.pack(side="left", padx=(12, 5), pady=10)
        self.text = tk.Label(self, text="Codex\n\u8fde\u63a5\u4e2d...", justify="left", anchor="w", wraplength=260, font=("Segoe UI", self.settings["font_size"]), fg=self.settings["font_color"], bg=self.settings["background_color"])
        self.text.pack(side="left", fill="both", expand=True, pady=10)
        self.bind("<Button-3>", self.menu)
        self.bind("<Enter>", self._pointer_enter)
        self.bind("<Leave>", self._pointer_leave)
        for widget in (self.face, self.text):
            widget.bind("<Button-3>", self.menu)
            widget.bind("<Enter>", self._pointer_enter)
            widget.bind("<Leave>", self._pointer_leave)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<ButtonRelease-1>", self.finish_drag)
        self._drag = (0, 0)
        self.apply_settings(self.settings)
        self.tray = TrayIcon3(self.tray_actions)
        self.after(100, self.process_tray_actions)
        self.after(250, self.poll)
        self.after(1000, self.refresh)

    def load_settings(self):
        settings, warnings = load_settings_api(self.settings_path)
        for warning in warnings:
            logging.getLogger("codex-status-pet").warning(warning)
        return settings

    def safe_position(self, x, y):
        """Preserve user-supplied virtual-desktop coordinates, including monitor 2."""
        try:
            return int(x), int(y)
        except (TypeError, ValueError):
            return 30, 120

    def save_settings(self):
        try:
            save_settings_atomic(self.settings_path, self.settings)
            return True
        except OSError:
            logging.getLogger("codex-status-pet").exception("failed to save settings")
            return False

    def apply_settings(self, settings):
        self.settings = dict(settings)
        if hasattr(self, "refresh_scheduler"):
            self.refresh_scheduler.set_interval(self.settings["refresh_interval_seconds"])
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.geometry(f"{self.settings['window_width']}x{self.settings['window_height']}+{self.settings['x']}+{self.settings['y']}")
        self.attributes("-alpha", self.settings["alpha"])
        self.attributes("-topmost", self.settings["topmost"])
        bg, fg = self.settings["background_color"], self.settings["font_color"]
        self.configure(bg=bg)
        self.face.configure(bg=bg, fg=fg)
        self.text.configure(bg=bg, fg=fg, font=("Segoe UI", self.settings["font_size"]))
        self.topmost_var.set(self.settings["topmost"])
        self.locked_var.set(self.settings["locked"])

    def _pointer_enter(self, _event=None):
        self.hovered = True
        if self.compact:
            self.set_compact(False)

    def _pointer_leave(self, _event=None):
        self.hovered = False

    def set_compact(self, compact):
        compact = bool(compact)
        if compact == self.compact or self.closing:
            return
        self.compact = compact
        if compact:
            self.text.pack_forget()
            self.face.pack_forget()
            self.face.pack(expand=True, padx=8, pady=8)
            size = compact_size(self.settings["window_width"], self.settings["window_height"])
        else:
            self.face.pack_forget()
            self.face.pack(side="left", padx=(12, 5), pady=10)
            self.text.pack(side="left", fill="both", expand=True, pady=10)
            size = None
        x, y = self.settings["x"], self.settings["y"]
        geometry = f"{size}x{size}+{x}+{y}" if size else f"{self.settings['window_width']}x{self.settings['window_height']}+{x}+{y}"
        self.geometry(geometry)

    def show_window(self):
        if self.compact:
            self.set_compact(False)
        x, y = self.hidden_position if self.hidden else (self.settings["x"], self.settings["y"])
        x, y = self.safe_position(x, y)
        self.settings["x"], self.settings["y"] = x, y
        self.hidden_position = (x, y)
        self.geometry(f"+{x}+{y}")
        self.hidden = False
        self.state("normal")
        self.deiconify()
        self.update_idletasks()
        self.attributes("-alpha", self.settings["alpha"])
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        def restore_topmost():
            if not self.closing:
                try:
                    self.attributes("-topmost", self.settings["topmost"])
                except tk.TclError:
                    logging.getLogger("codex-status-pet").debug("window closed before topmost restore")
        self.after(150, restore_topmost)

    def ensure_visible(self):
        """Restore the overlay after any settings-dialog focus/state transition."""
        if not self.closing:
            self.show_window()

    def hide_window(self):
        if not self.hidden:
            self.hidden_position = (self.settings["x"], self.settings["y"])
            self.settings["x"], self.settings["y"] = self.hidden_position
            self.save_settings()
        self.hidden = True
        self.attributes("-alpha", 0.0)

    def start_drag(self, event):
        if not self.settings["locked"]:
            self._drag = (event.x_root - self.winfo_rootx(), event.y_root - self.winfo_rooty())

    def drag(self, event):
        if not self.settings["locked"]:
            x = event.x_root - self._drag[0]
            y = event.y_root - self._drag[1]
            x, y = self.safe_position(x, y)
            self.geometry(f"+{x}+{y}")
            self.settings["x"], self.settings["y"] = x, y

    def finish_drag(self, _event):
        if not self.settings["locked"]:
            self.save_settings()

    def menu(self, event):
        """Show a native-looking Tk popup whose controls receive first-click events."""
        old_menu = getattr(self, "context_menu", None)
        if old_menu is not None:
            try:
                old_menu.grab_release()
                old_menu.destroy()
            except tk.TclError:
                pass

        popup = tk.Toplevel(self)
        self.context_menu = popup
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(bg="#e5e7eb")
        popup.geometry(f"+{event.x_root}+{event.y_root}")

        def close_popup():
            if getattr(self, "context_menu", None) is popup:
                self.context_menu = None
            try:
                popup.grab_release()
                popup.destroy()
            except tk.TclError:
                pass

        def run_and_close(command):
            close_popup()
            try:
                command()
            except Exception:
                logging.getLogger("codex-status-pet").exception("context-menu command failed")

        body = tk.Frame(popup, bg="#f3f4f6", bd=1, relief="solid")
        body.pack(padx=1, pady=1)
        button_options = {"anchor": "w", "width": 18, "bd": 0, "relief": "flat", "bg": "#f3f4f6", "activebackground": "#dbeafe"}
        for label, command in (
            ("立即刷新", self.refresh),
            ("显示设置", self.show_settings),
        ):
            tk.Button(body, text=label, command=lambda c=command: run_and_close(c), **button_options).pack(fill="x", padx=2, pady=1)
        tk.Checkbutton(body, text="置顶", variable=self.topmost_var, command=lambda: run_and_close(self.toggle_topmost), **button_options).pack(fill="x", padx=2, pady=1)
        tk.Checkbutton(body, text="锁定位置", variable=self.locked_var, command=lambda: run_and_close(self.toggle_locked), **button_options).pack(fill="x", padx=2, pady=1)
        tk.Frame(body, height=1, bg="#d1d5db").pack(fill="x", padx=2, pady=3)
        tk.Button(body, text="隐藏窗口", command=lambda: run_and_close(self.hide_window), **button_options).pack(fill="x", padx=2, pady=1)
        tk.Button(body, text="退出", command=lambda: run_and_close(self.close), **button_options).pack(fill="x", padx=2, pady=1)
        popup.bind("<Escape>", lambda _event: (close_popup(), "break")[1])
        popup.bind("<Button-3>", lambda _event: close_popup())
        popup.bind("<FocusOut>", lambda _event: popup.after_idle(close_popup))
        popup.update_idletasks()
        work_area = work_area_for_point(event.x_root, event.y_root)
        popup_x, popup_y = place_popup(
            event.x_root,
            event.y_root,
            popup.winfo_reqwidth(),
            popup.winfo_reqheight(),
            work_area,
        )
        popup.geometry(f"+{popup_x}+{popup_y}")
        popup.grab_set()
        popup.focus_force()
        return

        if getattr(self, "context_menu", None) is not None:
            try:
                self.context_menu.destroy()
            except tk.TclError:
                pass
        menu = tk.Menu(self, tearoff=0)
        self.context_menu = menu

        def close_menu():
            if getattr(self, "context_menu", None) is menu:
                self.context_menu = None
            try:
                menu.grab_release()
                menu.unpost()
                menu.destroy()
            except tk.TclError:
                pass

        def run_and_close(command):
            command()
            close_menu()

        menu.add_command(label="\u7acb\u5373\u5237\u65b0", command=lambda: run_and_close(self.refresh))
        menu.add_command(label="\u663e\u793a\u8bbe\u7f6e", command=lambda: run_and_close(self.show_settings))
        menu.add_checkbutton(label="\u7f6e\u9876", variable=self.topmost_var, command=lambda: run_and_close(self.toggle_topmost))
        menu.add_checkbutton(label="\u9501\u5b9a\u4f4d\u7f6e", variable=self.locked_var, command=lambda: run_and_close(self.toggle_locked))
        menu.add_separator()
        menu.add_command(label="\u9690\u85cf\u7a97\u53e3", command=lambda: run_and_close(self.hide_window))
        menu.add_command(label="\u9000\u51fa", command=lambda: run_and_close(self.close))

        # Some Windows Tk builds consume the first mouse release while the
        # posted menu is acquiring focus. Handle the release at widget level
        # so the first click always invokes the selected entry exactly once.
        def invoke_first_click(click_event):
            try:
                index = menu.index(f"@{click_event.y}")
                if index is not None and menu.type(index) not in ("separator", None):
                    menu.invoke(index)
                    return "break"
            except tk.TclError:
                pass
            return None

        menu.bind("<ButtonRelease-1>", invoke_first_click, add="+")
        menu.post(event.x_root, event.y_root)
        menu.grab_set()

    def toggle_topmost(self):
        self.settings["topmost"] = bool(self.topmost_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def toggle_locked(self):
        self.settings["locked"] = bool(self.locked_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def show_settings(self):
        if self.settings_dialog is not None and self.settings_dialog.winfo_exists():
            self.show_window()
            self.settings_dialog.deiconify()
            self.settings_dialog.lift()
            self.settings_dialog.focus_force()
            return
        self.show_window()
        dialog = tk.Toplevel(self)
        self.settings_dialog = dialog
        dialog.title("Codex \u5ba0\u7269\u8bbe\u7f6e")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        draft = dict(self.settings)
        body = tk.Frame(dialog, padx=14, pady=12)
        body.pack(fill="both", expand=True)
        alpha = tk.DoubleVar(value=draft["alpha"])
        size = tk.IntVar(value=draft["font_size"])
        position_x = tk.StringVar(value=str(draft["x"]))
        position_y = tk.StringVar(value=str(draft["y"]))
        window_width = tk.StringVar(value=str(draft["window_width"]))
        window_height = tk.StringVar(value=str(draft["window_height"]))
        refresh_interval = tk.StringVar(value=str(draft["refresh_interval_seconds"]))
        scale_mode = tk.StringVar(value=draft.get("scale_mode", "free"))
        topmost = tk.BooleanVar(value=draft["topmost"])
        locked = tk.BooleanVar(value=draft["locked"])
        compact_when_idle = tk.BooleanVar(value=draft["compact_when_idle"])

        tk.Label(body, text="\u900f\u660e\u5ea6").grid(row=0, column=0, sticky="w")
        tk.Scale(body, from_=0.25, to=1.0, resolution=0.05, orient="horizontal", length=230, variable=alpha).grid(row=0, column=1)
        tk.Label(body, text="\u5b57\u4f53\u5927\u5c0f").grid(row=1, column=0, sticky="w")
        tk.Scale(body, from_=8, to=20, resolution=1, orient="horizontal", length=230, variable=size).grid(row=1, column=1)
        tk.Label(body, text="\u9ed8\u8ba4\u4f4d\u7f6e (X, Y)").grid(row=2, column=0, sticky="w")
        position = tk.Frame(body)
        position.grid(row=2, column=1, sticky="w")
        digit_or_signed = (self.register(lambda value: value == "" or value.lstrip("+-").isdigit()), "%P")
        digits_only = (self.register(lambda value: value == "" or value.isdigit()), "%P")
        tk.Entry(position, textvariable=position_x, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
        tk.Label(position, text=", ").pack(side="left")
        tk.Entry(position, textvariable=position_y, width=8, validate="key", validatecommand=digit_or_signed).pack(side="left")
        tk.Label(body, text="窗口大小 (宽, 高)").grid(row=3, column=0, sticky="w")
        dimensions = tk.Frame(body)
        dimensions.grid(row=3, column=1, sticky="w")
        tk.Entry(dimensions, textvariable=window_width, width=8, validate="key", validatecommand=digits_only).pack(side="left")
        tk.Label(dimensions, text=", ").pack(side="left")
        tk.Entry(dimensions, textvariable=window_height, width=8, validate="key", validatecommand=digits_only).pack(side="left")
        def resize_by(factor):
            try:
                width, height = resize_dimensions(
                    window_width.get(),
                    window_height.get(),
                    factor,
                    proportional=scale_mode.get() == "proportional",
                )
            except ValueError:
                return
            window_width.set(width)
            window_height.set(height)
        tk.Button(dimensions, text="−", width=2, command=lambda: resize_by(0.9)).pack(side="left", padx=(6, 0))
        tk.Button(dimensions, text="+", width=2, command=lambda: resize_by(1.1)).pack(side="left")
        tk.Checkbutton(body, text="等比例缩放", variable=scale_mode, onvalue="proportional", offvalue="free").grid(row=4, column=0, sticky="w")
        tk.Label(body, text="刷新间隔 (秒)").grid(row=4, column=1, sticky="e")
        tk.Entry(body, textvariable=refresh_interval, width=8, validate="key", validatecommand=digits_only).grid(row=4, column=1, sticky="w", padx=(100, 0))
        tk.Checkbutton(body, text="\u7f6e\u9876", variable=topmost).grid(row=5, column=0, sticky="w")
        tk.Checkbutton(body, text="\u9501\u5b9a\u4f4d\u7f6e", variable=locked).grid(row=5, column=1, sticky="w")
        tk.Checkbutton(body, text="空闲时收缩", variable=compact_when_idle).grid(row=6, column=0, sticky="w")

        def choose_font():
            chosen = colorchooser.askcolor(color=draft["font_color"], parent=dialog)[1]
            if chosen:
                draft["font_color"] = chosen

        def choose_background():
            chosen = colorchooser.askcolor(color=draft["background_color"], parent=dialog)[1]
            if chosen:
                draft["background_color"] = chosen

        tk.Button(body, text="\u5b57\u4f53\u989c\u8272...", command=choose_font).grid(row=7, column=0, pady=(8, 0), sticky="w")
        tk.Button(body, text="\u80cc\u666f\u989c\u8272...", command=choose_background).grid(row=7, column=1, pady=(8, 0), sticky="w")

        def sync_draft():
            try:
                draft["alpha"] = float(alpha.get())
                draft["font_size"] = int(size.get())
                draft["x"] = int(position_x.get())
                draft["y"] = int(position_y.get())
                draft["window_width"] = min(1200, max(180, int(window_width.get())))
                draft["window_height"] = min(800, max(80, int(window_height.get())))
                draft["refresh_interval_seconds"] = min(10, max(1, int(refresh_interval.get())))
                draft["scale_mode"] = scale_mode.get()
                draft["topmost"] = bool(topmost.get())
                draft["locked"] = bool(locked.get())
                draft["compact_when_idle"] = bool(compact_when_idle.get())
            except (TypeError, ValueError):
                messagebox.showerror("设置无效", "坐标、窗口尺寸和刷新间隔必须填写合法数字。", parent=dialog)
                return False
            return True

        def apply_draft():
            if not sync_draft():
                return False
            self.apply_settings(draft)
            return True

        def save_and_close():
            if not apply_draft():
                return
            self.save_settings()
            self.close_settings(dialog)

        def restore_defaults():
            draft.clear()
            draft.update(DEFAULT_SETTINGS)
            alpha.set(draft["alpha"])
            size.set(draft["font_size"])
            position_x.set(draft["x"])
            position_y.set(draft["y"])
            window_width.set(draft["window_width"])
            window_height.set(draft["window_height"])
            refresh_interval.set(draft["refresh_interval_seconds"])
            scale_mode.set(draft["scale_mode"])
            topmost.set(draft["topmost"])
            locked.set(draft["locked"])
            compact_when_idle.set(draft["compact_when_idle"])

        buttons = tk.Frame(body)
        buttons.grid(row=8, column=0, columnspan=2, pady=(14, 0))
        tk.Button(buttons, text="\u4fdd\u5b58", width=8, command=save_and_close).pack(side="left", padx=3)
        tk.Button(buttons, text="\u5e94\u7528", width=8, command=apply_draft).pack(side="left", padx=3)
        tk.Button(buttons, text="\u6062\u590d\u9ed8\u8ba4\u503c", width=12, command=restore_defaults).pack(side="left", padx=3)
        tk.Button(buttons, text="\u5173\u95ed", width=8, command=lambda: self.close_settings(dialog)).pack(side="left", padx=3)
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.close_settings(dialog))
        dialog.update_idletasks()
        # Keep recovery settings reachable even when the saved overlay monitor
        # is disconnected or its virtual-desktop coordinates are off-screen.
        dialog_work_area = work_area_for_point(self.winfo_rootx(), self.winfo_rooty())
        dialog_x, dialog_y = place_popup(
            self.winfo_rootx(),
            self.winfo_rooty(),
            dialog.winfo_reqwidth(),
            dialog.winfo_reqheight(),
            dialog_work_area,
        )
        dialog.geometry(f"+{dialog_x}+{dialog_y}")
        dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
        self.after_idle(self.ensure_visible)

    def close_settings(self, dialog):
        if dialog is not None and dialog.winfo_exists():
            dialog.destroy()
        if self.settings_dialog is dialog:
            self.settings_dialog = None
        self.after_idle(self.ensure_visible)

    def process_tray_actions(self):
        if self.closing:
            return
        try:
            while True:
                action = self.tray_actions.get_nowait()
                if not is_known_action(action):
                    logging.getLogger("codex-status-pet").warning("unknown tray action: %r", action)
                    continue
                if action == "show":
                    self.show_window()
                elif action == "hide":
                    self.hide_window()
                elif action == "tray_menu":
                    event = type("TrayEvent", (), {
                        "x_root": self.winfo_pointerx(),
                        "y_root": self.winfo_pointery(),
                    })()
                    self.menu(event)
                elif action == "settings":
                    self.show_window()
                    self.show_settings()
                elif action == "exit":
                    self.close()
                elif action == "tray_error":
                    self.text.config(text="Codex\n托盘图标异常", fg="#fca5a5")
                    if should_schedule_restart(action, self.tray_restart_scheduled, self.closing):
                        self.tray_restart_scheduled = True
                        self.after(2000, self.restart_tray)
        except queue.Empty:
            pass
        except Exception:
            logging.getLogger("codex-status-pet").exception("tray action failed")
        if not self.closing:
            self.after(100, self.process_tray_actions)

    def restart_tray(self):
        if self.closing:
            return
        try:
            self.tray = TrayIcon3(self.tray_actions)
            self.tray_restart_scheduled = False
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon restart failed")
            self.after(5000, self.restart_tray)

    def refresh(self):
        if self.closing or not self.refresh_scheduler.begin():
            return
        def worker():
            try:
                if not self.server.proc or self.server.proc.poll() is not None:
                    self.server.start()
                payload = normalize_snapshot(self.server.read_limits())
                payload["_activity"] = self.activity.snapshot()
                self.queue.put(payload)
            except Exception as exc:
                self.queue.put({"error": str(exc)})
            finally:
                self.queue.put({"_refresh_done": True})
        threading.Thread(target=worker, daemon=True).start()

    def poll(self):
        if self.closing:
            return
        try:
            while True:
                payload = self.queue.get_nowait()
                if payload.get("_refresh_done"):
                    self.refresh_scheduler.finish()
                    if not self.closing:
                        self.after(self.refresh_scheduler.delay_ms, self.refresh)
                    continue
                if "error" in payload:
                    self.text.config(text="Codex\n" + payload["error"][:30], fg="#fca5a5")
                    continue
                limits = payload.get("rateLimits", {})
                primary, secondary = limits.get("primary", {}), limits.get("secondary", {})
                credits = payload.get("rateLimitResetCredits") or {}
                activity = payload.get("_activity", {"detail": "\u7a7a\u95f2", "progress": ""})
                active_count = activity.get("active", 0)
                if self.settings.get("compact_when_idle"):
                    self.set_compact(should_compact(True, active_count, self.hovered))
                credit_items = credits if isinstance(credits, (list, dict)) else []
                earliest_credit_expiry = earliest_future_expiry(credit_items)
                tier = health_tier(primary)
                text_color = self.settings["font_color"] if tier == "healthy" else HEALTH_COLORS.get(tier, self.settings["font_color"])
                self.text.config(text=(
                    f"Codex {activity.get('detail', '\u7a7a\u95f2')}\n"
                    f"{activity.get('progress', '')}\n"
                    f"5h {percent_left(primary)} / {short_time(primary.get('resetsAt'))}\n"
                    f"{quota_line('\u5468', percent_left(secondary), secondary.get('resetsAt'))}\n"
                    f"{reset_credit_line(credits.get('availableCount', '--') if isinstance(credits, dict) else '--', earliest_credit_expiry)}"
                ), fg=text_color)
        except queue.Empty:
            pass
        except Exception:
            logging.getLogger("codex-status-pet").exception("UI refresh payload failed")
        if not self.closing:
            self.after(250, self.poll)

    def close(self):
        if self.closing:
            return
        self.closing = True
        try:
            self.save_settings()
        except OSError:
            logging.getLogger("codex-status-pet").exception("failed to save settings during close")
        try:
            if hasattr(self, "tray"):
                self.tray.stop()
            self.server.stop()
        finally:
            self.destroy()
            if "_single_instance_guard" in globals():
                _single_instance_guard.release()


if __name__ == "__main__":
    if sys.platform != "win32":
        raise SystemExit("This tool is for Windows.")
    configure_logging(Path.home() / ".codex" / "codex-windows-status-pet.log")
    enable_dpi_awareness()
    if not ensure_single_instance():
        raise SystemExit(0)
    try:
        app = Pet()
        logging.getLogger("codex-status-pet").info(
            "display bounds=%s window_dpi=%s", virtual_desktop_bounds(), dpi_for_window(app.winfo_id())
        )
        app.mainloop()
    except Exception:
        logging.getLogger("codex-status-pet").exception("application startup or mainloop failure")
        if "_single_instance_guard" in globals():
            _single_instance_guard.release()
        raise
