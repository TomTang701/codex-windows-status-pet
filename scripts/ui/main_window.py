"""Windows Codex status overlay and notification-area companion."""

from __future__ import annotations

import logging
import queue
import sys
import threading
import time
import tkinter as tk
from pathlib import Path

APP_VERSION = "0.2.1"
try:
    from api.activity_api import snapshot_activity
    from api.codex_transport_api import AppServer
    from api.config_api import load_settings as load_settings_api, restore_settings_backup, save_settings_atomic
    from api.diagnostics_api import configure_logging
    from api.display_api import dpi_for_window, monitor_snapshot, virtual_desktop_bounds, work_area_for_point
    from api.diagnostic_summary_api import build_diagnostic_summary
    from api.status_snapshot_api import build_status_snapshot
    from api.refresh_scheduler_api import RefreshScheduler
    from api.refresh_controller_api import RefreshController
    from api.display_mode_api import compact_size
    from api.compact_state_api import CompactState, compact_geometry
    from api.window_recovery_api import recover_position
    from api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from api.quota_provider_api import normalize_snapshot
    from api.quota_state_api import QuotaState
    from api.runtime_api import SingleInstance, enable_dpi_awareness
    from ui.context_menu import show_context_menu
    from ui.settings_dialog import show_settings_dialog
    from ui.tray_adapter import TrayIcon3
except ModuleNotFoundError:
    from scripts.api.activity_api import snapshot_activity
    from scripts.api.codex_transport_api import AppServer
    from scripts.api.config_api import load_settings as load_settings_api, restore_settings_backup, save_settings_atomic
    from scripts.api.diagnostics_api import configure_logging
    from scripts.api.display_api import dpi_for_window, monitor_snapshot, virtual_desktop_bounds, work_area_for_point
    from scripts.api.diagnostic_summary_api import build_diagnostic_summary
    from scripts.api.status_snapshot_api import build_status_snapshot
    from scripts.api.refresh_scheduler_api import RefreshScheduler
    from scripts.api.refresh_controller_api import RefreshController
    from scripts.api.display_mode_api import compact_size
    from scripts.api.compact_state_api import CompactState, compact_geometry
    from scripts.api.window_recovery_api import recover_position
    from scripts.api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from scripts.api.quota_provider_api import normalize_snapshot
    from scripts.api.quota_state_api import QuotaState
    from scripts.api.runtime_api import SingleInstance, enable_dpi_awareness
    from scripts.ui.context_menu import show_context_menu
    from scripts.ui.settings_dialog import show_settings_dialog
    from scripts.ui.tray_adapter import TrayIcon3


def ensure_single_instance():
    """Claim the mutex without killing an existing process."""
    global _single_instance_guard
    _single_instance_guard = SingleInstance()
    return _single_instance_guard.acquire()


class ActivityMonitor:
    """Infer active turns from Codex session JSONL through the activity API."""

    def __init__(self):
        self.sessions = Path.home() / ".codex" / "sessions"
        self.stale_seconds = 600
        self.cache = {}

    def snapshot(self):
        return snapshot_activity(self.sessions, self.stale_seconds, cache=self.cache)




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
        self.expanded_position = (self.settings["x"], self.settings["y"])
        self.compact = False
        self.compact_state = CompactState()
        self._next_window_recovery = 0.0
        self.hovered = False
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.queue = queue.Queue()
        self.tray_actions = queue.Queue()
        self.settings_dialog = None
        self.tray_restart_scheduled = False
        self.server = AppServer(self.queue)
        self.activity = ActivityMonitor()
        self.refresh_scheduler = RefreshScheduler(self.settings["refresh_interval_seconds"])
        self.refresh_controller = RefreshController(("activity", "quota"))
        self.latest_activity = {"active": 0, "detail": "空闲", "progress": ""}
        self.latest_quota = {"rateLimits": {}, "rateLimitResetCredits": {}}
        self.quota_state = QuotaState()
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
        self.after(1000, self.refresh_activity)
        self.after(1000, self.refresh)

    def load_settings(self):
        settings, warnings = load_settings_api(self.settings_path)
        for warning in warnings:
            logging.getLogger("codex-status-pet").warning(warning)
        return settings

    def safe_position(self, x, y):
        """Preserve legal virtual-desktop coordinates and recover disconnected displays."""
        try:
            x, y = int(x), int(y)
        except (TypeError, ValueError):
            return 30, 120
        fallback = virtual_desktop_bounds()
        if fallback:
            left, top, width, height = fallback
            fallback_area = (left, top, left + width, top + height)
        else:
            fallback_area = (0, 0, 1920, 1080)
        monitors = []
        try:
            from api.display_api import monitor_snapshot
            monitors = monitor_snapshot()
        except (ImportError, AttributeError, OSError):
            pass
        recovered_x, recovered_y, recovered = recover_position(
            x, y, self.settings.get("window_width", 330), self.settings.get("window_height", 138), monitors, fallback_area
        )
        if recovered:
            logging.getLogger("codex-status-pet").warning("saved window position was off-screen; recovered to (%s, %s)", recovered_x, recovered_y)
        return recovered_x, recovered_y

    def save_settings(self):
        try:
            save_settings_atomic(self.settings_path, self.settings)
            return True
        except OSError:
            logging.getLogger("codex-status-pet").exception("failed to save settings")
            return False

    def restore_settings_backup(self):
        """Restore the last valid settings sidecar and apply it to the running overlay."""
        try:
            if not restore_settings_backup(self.settings_path):
                logging.getLogger("codex-status-pet").warning("settings backup is unavailable or malformed")
                return False
            self.settings = self.load_settings()
            self.apply_settings(self.settings)
            return True
        except OSError:
            logging.getLogger("codex-status-pet").exception("failed to restore settings backup")
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
        if compact:
            work_area = work_area_for_point(x, y)
            x, y = compact_geometry(x, y, self.settings["window_width"], self.settings["window_height"], size, work_area)
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

    def recover_window_if_needed(self):
        """Re-evaluate placement after display or taskbar topology changes."""
        if self.closing or self.hidden or self.compact:
            return
        now = time.monotonic()
        if now < self._next_window_recovery:
            return
        self._next_window_recovery = now + 2.0
        x, y = self.safe_position(self.settings["x"], self.settings["y"])
        if (x, y) == (self.settings["x"], self.settings["y"]):
            return
        self.settings["x"], self.settings["y"] = x, y
        self.hidden_position = (x, y)
        self.expanded_position = (x, y)
        self.geometry(f"+{x}+{y}")
        self.save_settings()

    def hide_window(self):
        if not self.hidden:
            self.hidden_position = (self.settings["x"], self.settings["y"])
            self.settings["x"], self.settings["y"] = self.hidden_position
            self.save_settings()
        self.hidden = True
        self.attributes("-alpha", 0.0)

    def start_drag(self, event):
        if self.compact:
            self.set_compact(False)
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
        show_context_menu(self, event)

    def copy_diagnostics(self):
        summary = build_diagnostic_summary(
            version=APP_VERSION,
            settings_path=self.settings_path,
            log_path=Path.home() / ".codex" / "codex-windows-status-pet.log",
            activity_path=self.activity.sessions,
            app_server_running=bool(self.server.proc and self.server.proc.poll() is None),
            quota_state=self.quota_state.state,
            monitor_count=len(monitor_snapshot()),
            dpi=dpi_for_window(self.winfo_id()),
        )
        self.clipboard_clear()
        self.clipboard_append(summary)
        self.update()

    def toggle_topmost(self):
        self.settings["topmost"] = bool(self.topmost_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def toggle_locked(self):
        self.settings["locked"] = bool(self.locked_var.get())
        self.apply_settings(self.settings)
        self.save_settings()

    def show_settings(self):
        show_settings_dialog(self)

    def close_settings(self, dialog):
        if dialog is not None and dialog.winfo_exists() and getattr(self, "_settings_session", None) is not None:
            self.apply_settings(self._settings_session.close())
        if dialog is not None and dialog.winfo_exists():
            dialog.destroy()
        if self.settings_dialog is dialog:
            self.settings_dialog = None
        if getattr(self, "_settings_session", None) is not None:
            self._settings_session = None
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

    def refresh_activity(self):
        """Refresh local session activity independently from app-server quota."""
        if self.closing:
            return
        generation = self.refresh_controller.begin("activity")
        if generation is None:
            return

        def worker():
            try:
                self.queue.put({"_channel": "activity", "_generation": generation, "_activity": self.activity.snapshot()})
            except Exception as exc:
                self.queue.put({"_channel": "activity", "_generation": generation, "error": str(exc)})
            finally:
                self.queue.put({"_channel_done": "activity", "_generation": generation})

        threading.Thread(target=worker, name="codex-activity-refresh", daemon=True).start()

    def refresh(self):
        """Refresh app-server quota on the user-selected interval."""
        if self.closing or not self.refresh_scheduler.begin():
            return
        generation = self.refresh_controller.begin("quota")
        if generation is None:
            self.refresh_scheduler.finish()
            return

        def worker():
            try:
                if not self.server.proc or self.server.proc.poll() is not None:
                    self.server.start()
                payload = normalize_snapshot(self.server.read_limits())
                payload.update({"_channel": "quota", "_generation": generation})
                self.queue.put(payload)
            except Exception as exc:
                self.queue.put({"_channel": "quota", "_generation": generation, "error": str(exc)})
            finally:
                self.queue.put({"_channel_done": "quota", "_generation": generation})

        threading.Thread(target=worker, name="codex-quota-refresh", daemon=True).start()

    def render_status(self):
        presentation = build_status_snapshot(
            self.latest_activity, self.latest_quota, self.quota_state.state, self.settings["font_color"]
        )
        active_count = presentation["active_count"]
        blocked = bool(getattr(self, "context_menu", None)) or bool(self.settings_dialog and self.settings_dialog.winfo_exists())
        should_be_compact = self.compact_state.update(
            self.settings.get("compact_when_idle"), active_count, self.hovered, blocked
        )
        if should_be_compact != self.compact:
            self.set_compact(should_be_compact)
        self.text.config(text=presentation["text"], fg=presentation["color"])

    def poll(self):
        if self.closing:
            return
        try:
            while True:
                payload = self.queue.get_nowait()
                if payload.get("_channel_done"):
                    channel = payload["_channel_done"]
                    self.refresh_controller.finish(channel, payload.get("_generation"))
                    if channel == "quota":
                        self.refresh_scheduler.finish()
                        if not self.closing:
                            self.after(self.refresh_scheduler.delay_ms, self.refresh)
                    elif channel == "activity" and not self.closing:
                        self.after(1000, self.refresh_activity)
                    continue
                channel = payload.get("_channel")
                if channel and not self.refresh_controller.is_current(channel, payload.get("_generation")):
                    continue
                if channel == "activity":
                    self.latest_activity = payload.get("_activity", self.latest_activity)
                elif channel == "quota":
                    if "error" in payload:
                        self.quota_state.fail("transport_error")
                        if self.quota_state.last_good is not None:
                            self.latest_quota = self.quota_state.last_good
                        self.text.config(text="Codex\n" + payload["error"][:30], fg="#fca5a5")
                        continue
                    if payload.get("status") == "available":
                        self.quota_state.update(payload)
                        self.latest_quota = payload
                    else:
                        self.quota_state.fail("unavailable")
                self.render_status()
        except queue.Empty:
            pass
        except Exception:
            logging.getLogger("codex-status-pet").exception("UI refresh payload failed")
        self.recover_window_if_needed()
        if not self.closing:
            self.after(250, self.poll)

    def close(self):
        if self.closing:
            return
        self.closing = True
        self.compact_state.force_expanded()
        if hasattr(self, "refresh_controller"):
            self.refresh_controller.shutdown()
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


def run():
    """Start the Windows companion after platform, logging, and mutex checks."""
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


if __name__ == "__main__":
    run()
