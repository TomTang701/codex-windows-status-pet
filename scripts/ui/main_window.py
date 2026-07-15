"""Windows Codex status overlay and notification-area companion."""

from __future__ import annotations

import logging
import queue
import sys
import threading
import time
import tkinter as tk
from datetime import datetime, timezone
from pathlib import Path

APP_VERSION = "0.9.1"
try:
    from api.activity_api import snapshot_activity
    from api.codex_transport_api import AppServer
    from api.application_controller_api import ApplicationController
    from api.config_api import ConfigWriteProtectedError
    from api.diagnostics_api import configure_logging
    from api.display_api import dpi_for_window, monitor_for_point, monitor_snapshot, virtual_desktop_bounds, work_area_for_point
    from api.diagnostic_summary_api import build_diagnostic_summary
    from api.display_mode_api import compact_size
    from api.compact_state_api import canonical_expanded_position, compact_geometry
    from api.settings_persistence_controller_api import SettingsPersistenceController
    from api.status_presentation_controller_api import StatusPresentationController
    from api.window_lifecycle_controller_api import WindowLifecycleController
    from api.window_recovery_api import recover_position
    from api.window_scale_api import derive_window_metrics
    from api.localization_api import translate
    from api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from api.quota_parse_api import parse_quota_payload
    from api.quota_state_api import QuotaState
    from api.runtime_api import SingleInstance, enable_dpi_awareness, ensure_overlay_toolwindow
    from ui.context_menu import show_context_menu
    from ui.battery_view import BatteryView
    from ui.settings_dialog import show_settings_dialog
    from ui.status_rows import StatusRows
    from ui.tray_adapter import TrayIcon3
    from ui.theme import COLORS, FONT_FAMILY
except ModuleNotFoundError:
    from scripts.api.activity_api import snapshot_activity
    from scripts.api.codex_transport_api import AppServer
    from scripts.api.application_controller_api import ApplicationController
    from scripts.api.config_api import ConfigWriteProtectedError
    from scripts.api.diagnostics_api import configure_logging
    from scripts.api.display_api import dpi_for_window, monitor_for_point, monitor_snapshot, virtual_desktop_bounds, work_area_for_point
    from scripts.api.diagnostic_summary_api import build_diagnostic_summary
    from scripts.api.display_mode_api import compact_size
    from scripts.api.compact_state_api import canonical_expanded_position, compact_geometry
    from scripts.api.settings_persistence_controller_api import SettingsPersistenceController
    from scripts.api.status_presentation_controller_api import StatusPresentationController
    from scripts.api.window_lifecycle_controller_api import WindowLifecycleController
    from scripts.api.window_recovery_api import recover_position
    from scripts.api.window_scale_api import derive_window_metrics
    from scripts.api.localization_api import translate
    from scripts.api.tray_lifecycle_api import is_known_action, should_schedule_restart
    from scripts.api.quota_parse_api import parse_quota_payload
    from scripts.api.quota_state_api import QuotaState
    from scripts.api.runtime_api import SingleInstance, enable_dpi_awareness, ensure_overlay_toolwindow
    from scripts.ui.context_menu import show_context_menu
    from scripts.ui.battery_view import BatteryView
    from scripts.ui.settings_dialog import show_settings_dialog
    from scripts.ui.status_rows import StatusRows
    from scripts.ui.tray_adapter import TrayIcon3
    from scripts.ui.theme import COLORS, FONT_FAMILY


def ensure_single_instance():
    """Claim the mutex without killing an existing process."""
    global _single_instance_guard
    _single_instance_guard = SingleInstance()
    return _single_instance_guard.acquire()


def existing_instance_notice(language):
    """Return the single-instance notice through the runtime localization authority."""
    return translate(language, "existing_instance")


def notify_existing_instance():
    """Explain why a windowed second launch exits without opening a window."""
    language = "en"
    try:
        language = SettingsPersistenceController(
            Path.home() / ".codex" / "codex-windows-status-pet.json"
        ).load().settings["language"]
    except (KeyError, OSError):
        pass
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(
            None,
            existing_instance_notice(language),
            "Codex Windows Status Pet",
            0x10,
        )
    except (AttributeError, OSError):
        logging.getLogger("codex-status-pet").warning(
            "an existing application instance prevented startup"
        )


class ActivityMonitor:
    """Infer active turns from Codex session JSONL through the activity API."""

    def __init__(self):
        self.sessions = Path.home() / ".codex" / "sessions"
        self.stale_seconds = 600
        self.cache = {}

    def snapshot(self):
        return snapshot_activity(self.sessions, self.stale_seconds, cache=self.cache)




class Pet(tk.Tk):
    @property
    def closing(self):
        return getattr(self, "lifecycle", None) is not None and self.lifecycle.closing

    @property
    def settings_path(self):
        controller = getattr(self, "settings_controller", None)
        return controller.path if controller is not None else self._settings_path

    @settings_path.setter
    def settings_path(self, path):
        self._settings_path = Path(path)
        controller = getattr(self, "settings_controller", None)
        if controller is not None:
            controller.set_path(self._settings_path)

    @property
    def refresh_controller(self):
        """Compatibility view; coordination ownership lives in ApplicationController."""
        return self.application_controller.refresh

    @property
    def refresh_scheduler(self):
        """Compatibility view; scheduling ownership lives in ApplicationController."""
        return self.application_controller.quota

    @property
    def compact_state(self):
        """Compatibility view for the explicit manual compact setting."""
        return self.compact

    def __init__(self):
        super().__init__()
        self.withdraw()
        self.lifecycle = WindowLifecycleController()
        self.title("Codex Windows Status Pet")
        self.overrideredirect(True)
        self.settings_path = Path.home() / ".codex" / "codex-windows-status-pet.json"
        self.settings_controller = SettingsPersistenceController(self.settings_path)
        self.settings = self.load_settings()
        self._sync_compatibility_metrics(self.settings)
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.geometry(f"+{self.settings['x']}+{self.settings['y']}")
        self.update_idletasks()
        self._sync_compatibility_metrics(self.settings)
        self.configure(
            bg=self.settings["background_color"],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
        )
        self.geometry(f"{self.window_metrics.width}x{self.window_metrics.height}+{self.settings['x']}+{self.settings['y']}")
        self.hidden = False
        self.hidden_position = (self.settings["x"], self.settings["y"])
        self.expanded_position = (self.settings["x"], self.settings["y"])
        self.compact = False
        self.presentation_controller = StatusPresentationController()
        self._next_window_recovery = 0.0
        self.hovered = False
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.queue = queue.Queue()
        self.tray_actions = queue.Queue()
        self.settings_dialog = None
        self.tray_restart_scheduled = False
        self.server = AppServer(self.queue)
        self.activity = ActivityMonitor()
        self.application_controller = ApplicationController(self.settings["refresh_interval_seconds"])
        self.latest_activity = {"active": 0, "detail": "空闲", "progress": ""}
        self.latest_quota = {"rateLimits": {}, "rateLimitResetCredits": {}}
        self.quota_state = QuotaState()
        self.topmost_var = tk.BooleanVar(value=self.settings["topmost"])
        self.locked_var = tk.BooleanVar(value=self.settings["locked"])
        self.compact_var = tk.BooleanVar(value=self.settings["compact"])
        hud_bg = self.settings["background_color"]
        self.hud_header = tk.Frame(self, bg=COLORS["surface_alt"], height=11, highlightthickness=1, highlightbackground=COLORS["border"])
        self.hud_header.pack_propagate(False)
        self.hud_title = tk.Label(self.hud_header, text="CODEX", bg=COLORS["surface_alt"], fg=COLORS["accent"], font=(FONT_FAMILY, 7, "bold"), anchor="w")
        self.hud_title.pack(side="left", padx=(8, 4), fill="y")
        self.status_title = tk.Label(
            self.hud_header,
            text=translate(self.settings["language"], "status"),
            bg=COLORS["surface_alt"],
            fg=COLORS["muted"],
            font=(FONT_FAMILY, 7),
            anchor="w",
        )
        self.status_title.pack(side="left", padx=(0, 4), fill="y")
        self.hud_status = tk.Label(self.hud_header, text=translate(self.settings["language"], "idle"), bg=COLORS["surface_alt"], fg=COLORS["muted"], font=(FONT_FAMILY, 7), anchor="e")
        self.hud_status.pack(side="right", padx=(4, 8), fill="y")
        self.hud_status_dot = tk.Label(
            self.hud_header,
            text=chr(0x25CB),
            bg=COLORS["surface_alt"],
            fg=COLORS["muted"],
            font=(FONT_FAMILY, 7),
            anchor="e",
        )
        self.hud_status_dot.pack(side="right", padx=(0, 2), fill="y")
        self.status_card = tk.Frame(self, bg=hud_bg, highlightthickness=1, highlightbackground=COLORS["border"])
        self.signal_card = tk.Frame(self, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
        self.status_rail = tk.Frame(self.status_card, bg=COLORS["border"], width=2)
        self.status_rail.place(x=1, y=1, width=2, relheight=1)
        self.signal_title = tk.Label(self.signal_card, text="SIGNAL", bg=COLORS["surface"], fg=COLORS["muted"], font=(FONT_FAMILY, 7, "bold"), anchor="w")
        self.signal_title.place(x=6, y=3, anchor="nw")
        self.signal_age = tk.Label(self.signal_card, text="Sync --", bg=COLORS["surface"], fg=COLORS["muted"], font=(FONT_FAMILY, 6), anchor="w")
        self.signal_value = tk.Label(self.signal_card, text="--", bg=COLORS["surface"], fg=COLORS["muted"], font=(FONT_FAMILY, 8, "bold"), anchor="e")
        self.signal_value.place(relx=1, rely=1, x=-6, y=-3, anchor="se")
        self.text = StatusRows(self.status_card, text="Codex\n\u8fde\u63a5\u4e2d...", wraplength=self.window_metrics.wraplength, font=self._font_spec(FONT_FAMILY, self.window_metrics.text_font_size), fg=self.settings["font_color"], bg=hud_bg)
        self.battery = BatteryView(self.signal_card, bg=COLORS["surface"])
        self._pack_expanded_content()
        self.bind("<Button-3>", self.menu)
        self.bind("<Enter>", self._pointer_enter)
        self.bind("<Leave>", self._pointer_leave)
        self._drag = (0, 0)
        for widget in self._hud_event_widgets():
            widget.bind("<Button-3>", self.menu)
            widget.bind("<Enter>", self._pointer_enter)
            widget.bind("<Leave>", self._pointer_leave)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<ButtonRelease-1>", self.finish_drag)
        self.apply_settings(self.settings)
        self.set_compact(self.settings["compact"])
        self.tray = TrayIcon3(self.tray_actions, self.settings["language"])
        self._sync_tray_menu()
        self.after(100, self.process_tray_actions)
        self.after(250, self.poll)
        self.after(1000, self.refresh_activity)
        self.after(1000, self.refresh)
        self.deiconify()
        ensure_overlay_toolwindow(self.winfo_id())

    def load_settings(self):
        result = self.settings_controller.load()
        for warning in result.warnings:
            logging.getLogger("codex-status-pet").warning(warning)
        return result.settings

    def safe_position(self, x, y, width=None, height=None):
        """Preserve legal virtual-desktop coordinates and recover disconnected displays."""
        try:
            x, y = int(x), int(y)
        except (TypeError, ValueError):
            return 30, 120
        fallback = virtual_desktop_bounds()
        if fallback:
            left, top, desktop_width, desktop_height = fallback
            fallback_area = (left, top, left + desktop_width, top + desktop_height)
        else:
            fallback_area = (0, 0, 1920, 1080)
        monitors = []
        try:
            from api.display_api import monitor_snapshot
            monitors = monitor_snapshot()
        except (ImportError, AttributeError, OSError):
            pass
        metrics = getattr(self, "window_metrics", derive_window_metrics(self.settings.get("window_scale_percent")))
        if width is None or height is None:
            target_monitor = monitor_for_point(x, y, monitors)
            recovery_metrics = metrics
            if target_monitor is not None:
                recovery_metrics = derive_window_metrics(
                    self.settings.get("window_scale_percent"),
                    dpi=target_monitor.get("dpi_x", self.window_dpi),
                )
            width, height = recovery_metrics.width, recovery_metrics.height
        recovered_x, recovered_y, recovered = recover_position(
            x, y, int(width), int(height), monitors, fallback_area
        )
        if recovered:
            logging.getLogger("codex-status-pet").warning("saved window position was off-screen; recovered to (%s, %s)", recovered_x, recovered_y)
        return recovered_x, recovered_y

    def save_settings(self, *, allow_unsafe_overwrite=False):
        try:
            return self.settings_controller.save(
                self.settings,
                allow_unsafe_overwrite=allow_unsafe_overwrite,
            )
        except ConfigWriteProtectedError as exc:
            logging.getLogger("codex-status-pet").warning("%s", exc)
            return False
        except OSError:
            logging.getLogger("codex-status-pet").exception("failed to save settings")
            return False

    def restore_settings_backup(self):
        """Restore the last valid settings sidecar and apply it to the running overlay."""
        try:
            if not self.settings_controller.restore_backup():
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
        self.window_metrics = derive_window_metrics(
            self.settings.get("window_scale_percent")
        )
        if hasattr(self, "application_controller"):
            self.application_controller.set_quota_interval(self.settings["refresh_interval_seconds"])
        if hasattr(self, "tray") and hasattr(self.tray, "set_language"):
            self.tray.set_language(self.settings["language"])
        self.settings["x"], self.settings["y"] = self.safe_position(self.settings["x"], self.settings["y"])
        self.geometry(f"+{self.settings['x']}+{self.settings['y']}")
        self.update_idletasks()
        metrics = self._sync_compatibility_metrics(self.settings)
        self.geometry(f"{metrics.width}x{metrics.height}+{self.settings['x']}+{self.settings['y']}")
        self.attributes("-alpha", self.settings["alpha"])
        self.attributes("-topmost", self.settings["topmost"])
        bg, fg = self.settings["background_color"], self.settings["font_color"]
        self.configure(bg=bg, highlightbackground=COLORS["border"], highlightcolor=COLORS["accent"])
        self.hud_header.configure(
            bg=COLORS["surface_alt"],
            highlightbackground=COLORS["border"],
            height=self._hud_header_height(),
        )
        header_font = self._font_spec(
            FONT_FAMILY,
            max(6, round(metrics.text_font_size * 0.7)),
        )
        self.hud_title.configure(font=(*header_font, "bold"))
        self.status_title.configure(font=header_font)
        self.hud_status.configure(font=header_font)
        self.hud_status_dot.configure(font=header_font)
        signal_title_font = self._font_spec(
            FONT_FAMILY,
            max(6, round(metrics.text_font_size * 0.7)),
        )
        signal_value_font = self._font_spec(
            FONT_FAMILY,
            max(7, round(metrics.text_font_size * 0.85)),
        )
        self.signal_title.configure(font=(*signal_title_font, "bold"))
        self.signal_age.configure(font=self._font_spec(FONT_FAMILY, max(5, round(metrics.text_font_size * 0.55))))
        self.signal_value.configure(font=(*signal_value_font, "bold"))
        header_padding = self._hud_header_padding()
        self.hud_title.pack_configure(padx=(header_padding, max(2, round(header_padding / 2))))
        self.status_title.pack_configure(padx=(0, max(2, round(header_padding / 2))))
        self.hud_status.pack_configure(padx=(max(2, round(header_padding / 2)), header_padding))
        self.hud_title.configure(bg=COLORS["surface_alt"])
        self.hud_status.configure(bg=COLORS["surface_alt"])
        self.hud_status_dot.configure(bg=COLORS["surface_alt"])
        self.status_card.configure(bg=bg, highlightbackground=COLORS["border"])
        self.status_rail.configure(bg=COLORS["border"])
        self.status_title.configure(
            bg=COLORS["surface_alt"],
            text=translate(self.settings["language"], "status"),
        )
        self.signal_card.configure(bg=COLORS["surface"], highlightbackground=COLORS["border"])
        self.signal_age.configure(bg=COLORS["surface"])
        source = self.settings["battery_quota_source"]
        self.signal_title.configure(
            bg=COLORS["surface"],
            text=self._signal_caption(source, self.settings["language"]),
            fg=COLORS["accent"] if source == "primary_5h" else COLORS["accent_alt"],
        )
        self.signal_value.configure(bg=COLORS["surface"], fg=COLORS["muted"])
        self._update_signal_age()
        active = bool(self.latest_activity.get("active", 0))
        self.hud_status.configure(
            text=translate(self.settings["language"], "output" if active else "idle"),
            fg=COLORS["success"] if active else COLORS["muted"],
        )
        self.hud_status_dot.configure(
            text=self._status_indicator("output" if active else "idle"),
            fg=COLORS["success"] if active else COLORS["muted"],
        )
        self.battery.configure(bg=COLORS["surface"])
        self.battery.set_metrics(metrics.text_font_size, compact=self.compact)
        self.text.set_visible_rows(self.settings)
        self.text.configure_rows(bg=bg, fg=fg, font=self._font_spec(FONT_FAMILY, metrics.text_font_size), wraplength=metrics.wraplength)
        self._sync_drag_cursor()
        if not self.compact:
            self._pack_expanded_content()
        self._apply_current_mode_geometry()
        self.topmost_var.set(self.settings["topmost"])
        self.locked_var.set(self.settings["locked"])
        if hasattr(self, "compact_var"):
            self.compact_var.set(self.settings["compact"])
        self._sync_tray_menu()

    def _sync_tray_menu(self):
        """Push a plain Tk-owned menu snapshot to the tray adapter."""
        tray = getattr(self, "tray", None)
        if tray is not None and hasattr(tray, "set_menu_state"):
            tray.set_menu_state(
                self.settings["language"],
                visible=not self.hidden,
                topmost=self.settings["topmost"],
                locked=self.settings["locked"],
                compact=self.settings["compact"],
            )

    def _pointer_enter(self, _event=None):
        self.hovered = True
        self._sync_hover_rail()

    def _pointer_leave(self, event=None):
        if event is not None:
            try:
                containing = self.winfo_containing(event.x_root, event.y_root)
                if containing is not None and containing.winfo_toplevel() == self:
                    self.hovered = True
                    self._sync_hover_rail()
                    return
            except tk.TclError:
                pass
        self.hovered = False
        self._sync_hover_rail()

    def _sync_hover_rail(self):
        """Give the draggable HUD a quiet hover affordance without changing status color."""
        width = 3 if self.hovered and not self.compact else 2
        try:
            self.status_rail.place_configure(width=width)
        except tk.TclError:
            pass

    def _sync_drag_cursor(self):
        """Expose whether the HUD can be dragged through its cursor affordance."""
        cursor = "arrow" if self.settings["locked"] else "fleur"
        self.configure(cursor=cursor)
        for widget in self._hud_event_widgets():
            widget.configure(cursor=cursor)

    def _hud_event_widgets(self):
        """Return all HUD surfaces that should share pointer interactions."""
        return (
            self.hud_header,
            self.hud_title,
            self.hud_status,
            self.hud_status_dot,
            self.status_card,
            self.status_rail,
            self.status_title,
            self.signal_card,
            self.signal_title,
            self.signal_age,
            self.signal_value,
            *self.text.event_widgets,
            *self.battery.event_widgets,
        )

    def _sync_compatibility_metrics(self, settings):
        logical = derive_window_metrics(settings.get("window_scale_percent"))
        self.window_dpi = dpi_for_window(self.winfo_id())
        display = derive_window_metrics(
            logical.scale_percent, dpi=self.window_dpi
        )
        settings["window_scale_percent"] = logical.scale_percent
        settings["font_size"] = logical.text_font_size
        settings["window_width"] = logical.width
        settings["window_height"] = logical.height
        settings["scale_mode"] = "proportional"
        self.window_metrics = display
        return display

    def _font_spec(self, family, logical_point_size):
        # CJK glyphs need a tighter fit only at the two smallest HUD sizes;
        # from 95% upward, 0.85 keeps the bilingual hierarchy closer to English.
        scale_percent = int(self.settings.get("window_scale_percent", 100))
        scale = (
            0.7 if scale_percent <= 90 else 0.85
        ) if self.settings.get("language") == "zh-CN" else 1.0
        pixels = max(1, round(logical_point_size * self.window_dpi / 72.0 * scale))
        return family, -pixels

    def _hud_header_height(self):
        """Keep the compact status header proportional to the active HUD scale."""
        metrics = getattr(self, "window_metrics", None)
        if metrics is None:
            return 11
        dpi_scale = self.window_dpi / 96.0 if self.window_dpi > 0 else 1.0
        return max(11, round(14 * metrics.scale_percent / 100 * dpi_scale))

    def _hud_header_padding(self):
        """Scale header breathing room with the same physical HUD ratio."""
        metrics = getattr(self, "window_metrics", None)
        if metrics is None:
            return 8
        dpi_scale = self.window_dpi / 96.0 if self.window_dpi > 0 else 1.0
        return max(4, round(8 * metrics.scale_percent / 100 * dpi_scale))

    def _pack_expanded_content(self):
        metrics = self.window_metrics
        self.hud_header.pack_forget()
        self.status_card.pack_forget()
        self.signal_card.pack_forget()
        self.battery.pack_forget()
        self.text.pack_forget()
        self.hud_header.configure(height=self._hud_header_height())
        self.hud_header.pack(side="top", fill="x", padx=metrics.horizontal_padding, pady=0)
        self.status_card.pack(side="left", fill="both", expand=True, padx=(metrics.horizontal_padding, 3), pady=0)
        self.signal_card.pack(side="right", fill="y", padx=(0, metrics.horizontal_padding), pady=0)
        self.signal_card.pack_propagate(False)
        self.signal_card.configure(width=self._signal_card_width())
        self._sync_hover_rail()
        inset = self._hud_header_padding()
        self.signal_title.place(x=inset, y=max(2, round(inset / 2)), anchor="nw")
        self.signal_age.place(x=inset, y=max(12, round(inset * 1.6)), anchor="nw")
        self.signal_value.place(
            relx=1,
            rely=1,
            x=-inset,
            y=-max(2, round(inset / 2)),
            anchor="se",
        )
        self.text.pack(
            fill="both",
            expand=True,
            padx=(metrics.horizontal_padding, metrics.face_text_gap),
            pady=0,
        )
        self.battery.pack(expand=True, padx=metrics.horizontal_padding, pady=2)
        self.signal_title.lift()
        self.signal_age.lift()
        self.signal_value.lift()

    def _apply_current_mode_geometry(self):
        """Apply root geometry from canonical settings in the current manual mode."""
        x, y = self.settings["x"], self.settings["y"]
        if self.compact:
            size = compact_size(self.window_metrics.width, self.window_metrics.height)
            work_area = work_area_for_point(x, y)
            x, y = compact_geometry(
                x,
                y,
                self.window_metrics.width,
                self.window_metrics.height,
                size,
                work_area,
            )
            self.geometry(f"{size}x{size}+{x}+{y}")
            return
        self.geometry(
            f"{self.window_metrics.width}x{self.window_metrics.height}+{x}+{y}"
        )

    def set_compact(self, compact):
        compact = bool(compact)
        if compact == self.compact or self.closing:
            return
        self.compact = compact
        if compact:
            self.hud_header.pack_forget()
            self.status_card.pack_forget()
            self.signal_card.pack_forget()
            self.signal_title.place_forget()
            self.signal_age.place_forget()
            self.signal_value.place_forget()
            self.text.pack_forget()
            self.battery.pack_forget()
            self.battery.set_compact(True)
            self.battery.set_metrics(self.window_metrics.text_font_size, compact=True)
            self.signal_card.pack(expand=True, fill="both", padx=0, pady=0)
            self.battery.pack(expand=True, padx=8, pady=8)
            size = compact_size(self.window_metrics.width, self.window_metrics.height)
        else:
            self.battery.set_compact(False)
            self.battery.set_metrics(self.window_metrics.text_font_size, compact=False)
            self._pack_expanded_content()
            size = None
        self._apply_current_mode_geometry()

    def set_manual_compact(self, compact):
        """Apply the only normal compact authority and persist it immediately."""
        compact = bool(compact)
        self.settings["compact"] = compact
        self.compact_var.set(compact)
        self.set_compact(compact)
        self._sync_tray_menu()
        return self.save_settings()

    def show_window(self):
        x, y = self.hidden_position if self.hidden else (self.settings["x"], self.settings["y"])
        x, y = self.safe_position(x, y)
        self.settings["x"], self.settings["y"] = x, y
        self.hidden_position = (x, y)
        self.geometry(f"+{x}+{y}")
        self.hidden = False
        self.state("normal")
        self.deiconify()
        ensure_overlay_toolwindow(self.winfo_id())
        self.update_idletasks()
        self.attributes("-alpha", self.settings["alpha"])
        self._sync_tray_menu()
        settings_dialog_open = (
            self.settings_dialog is not None
            and self.settings_dialog.winfo_exists()
        )
        if settings_dialog_open:
            self.attributes("-topmost", False)
            self.settings_dialog.attributes("-topmost", True)
            self.settings_dialog.lift()
            self.settings_dialog.focus_force()
            return
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        def restore_topmost():
            if not self.closing:
                try:
                    if self.settings_dialog is not None and self.settings_dialog.winfo_exists():
                        self.attributes("-topmost", False)
                        return
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
        self._sync_tray_menu()

    def start_drag(self, event):
        if not self.settings["locked"]:
            self._drag = (event.x_root - self.winfo_rootx(), event.y_root - self.winfo_rooty())

    def drag(self, event):
        if not self.settings["locked"]:
            x = event.x_root - self._drag[0]
            y = event.y_root - self._drag[1]
            if self.compact:
                size = compact_size(self.window_metrics.width, self.window_metrics.height)
                x, y = self.safe_position(x, y, size, size)
                work_area = work_area_for_point(x, y)
                canonical_x, canonical_y = canonical_expanded_position(
                    x,
                    y,
                    self.window_metrics.width,
                    self.window_metrics.height,
                    size,
                    work_area,
                )
                self.settings["x"], self.settings["y"] = self.safe_position(
                    canonical_x, canonical_y
                )
                self._apply_current_mode_geometry()
                return
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
                elif action == "topmost":
                    self.topmost_var.set(not self.settings["topmost"])
                    self.toggle_topmost()
                elif action == "lock":
                    self.locked_var.set(not self.settings["locked"])
                    self.toggle_locked()
                elif action == "compact":
                    self.set_manual_compact(not self.settings["compact"])
                elif action == "exit":
                    self.close()
                elif action == "tray_error":
                    presentation = self.presentation_controller.render_tray_error()
                    self.configure(highlightbackground=COLORS["danger"])
                    self.text.configure_rows(
                        rows=presentation["rows"], fg=presentation["color"]
                    )
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
            self.tray = TrayIcon3(self.tray_actions, self.settings["language"])
            self.tray_restart_scheduled = False
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon restart failed")
            self.after(5000, self.restart_tray)

    def refresh_activity(self):
        """Refresh local session activity independently from app-server quota."""
        if self.closing:
            return
        generation = self.application_controller.begin_activity()
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
        if self.closing:
            return
        generation = self.application_controller.begin_quota()
        if generation is None:
            return

        def worker():
            try:
                if not self.server.proc or self.server.proc.poll() is not None:
                    self.server.start()
                payload = parse_quota_payload(self.server.read_limits())
                payload.update({"_channel": "quota", "_generation": generation})
                self.queue.put(payload)
            except Exception as exc:
                self.queue.put({"_channel": "quota", "_generation": generation, "error": str(exc)})
            finally:
                self.queue.put({"_channel_done": "quota", "_generation": generation})

        threading.Thread(target=worker, name="codex-quota-refresh", daemon=True).start()

    def render_status(self):
        presentation = self.presentation_controller.render(
            self.latest_activity,
            self.latest_quota,
            self.quota_state.state,
            self.settings["font_color"],
            self.settings["battery_quota_source"],
            self.settings["language"],
        )
        border_color = self._hud_border_color(presentation)
        self.configure(highlightbackground=border_color)
        self.hud_header.configure(highlightbackground=border_color)
        self.status_card.configure(highlightbackground=border_color)
        self.signal_card.configure(highlightbackground=border_color)
        self.status_rail.configure(bg=border_color)
        active = bool(presentation.get("active_count", 0))
        quota_state = presentation.get("quota_state")
        status_key = (
            "quota_unavailable" if quota_state in {"unavailable", "tray_error"}
            else "stale" if quota_state == "stale"
            else "output" if active
            else "idle"
        )
        status_color = (
            COLORS["danger"] if quota_state in {"unavailable", "tray_error"}
            else COLORS["muted"] if quota_state == "stale"
            else COLORS["success"] if active
            else COLORS["muted"]
        )
        self.hud_status.configure(
            text=translate(self.settings["language"], status_key),
            fg=status_color,
        )
        self.hud_status_dot.configure(
            text=self._status_indicator(status_key),
            fg=status_color,
        )
        self._update_signal_age(quota_state)
        battery = presentation["battery"]
        remaining = battery.get("remaining_percent")
        self.signal_value.configure(
            text="--" if remaining is None else f"{remaining}%",
            fg=self._signal_value_color(
                remaining,
                self.settings["battery_quota_source"],
            ),
        )
        self.text.configure_rows(rows=presentation["rows"], fg=presentation["color"])
        self.battery.configure_presentation(presentation["battery"])

    @staticmethod
    def _hud_border_color(presentation):
        """Use the HUD outline as a low-noise live status indicator."""
        if presentation.get("quota_state") in {"unavailable", "tray_error"}:
            return COLORS["danger"]
        if presentation.get("quota_state") == "stale":
            return COLORS["muted"]
        if presentation.get("quota_tier") == "critical":
            return COLORS["danger"]
        if presentation.get("quota_tier") == "caution":
            return COLORS["warning"]
        if presentation.get("active_count", 0):
            return COLORS["success"]
        return COLORS["border"]

    def _signal_card_width(self):
        metrics = getattr(self, "window_metrics", None)
        if metrics is None:
            return 68
        dpi_scale = self.window_dpi / 96.0 if self.window_dpi > 0 else 1.0
        return max(54, round(68 * metrics.scale_percent / 100 * dpi_scale))

    def _update_signal_age(self, quota_state=None):
        state = quota_state or self.quota_state.state
        prefix = "Sync" if self.settings.get("language") == "en" else chr(0x540C) + chr(0x6B65)
        timestamp = self.quota_state.last_success_at
        if timestamp is None:
            age_text = "--"
        else:
            age = max(0, int((datetime.now(timezone.utc) - timestamp).total_seconds()))
            age_text = f"{age}s"
        self.signal_age.configure(
            text=f"{prefix} {age_text}",
            fg=COLORS["danger"] if state in {"unavailable", "tray_error"} else COLORS["muted"],
        )

    @staticmethod
    def _status_indicator(status_key):
        return {
            "output": chr(0x25CF),
            "idle": chr(0x25CB),
            "stale": chr(0x25D0),
            "quota_unavailable": "!",
            "tray_error": "!",
        }.get(status_key, chr(0x25CB))

    @staticmethod
    def _signal_caption(source, language):
        return translate(language, "five_hour" if source == "primary_5h" else "weekly")

    @staticmethod
    def _signal_value_color(remaining, source):
        """Use source color while healthy and health colors as quota gets low."""
        if remaining is None or remaining < 10:
            return COLORS["danger"]
        if remaining < 50:
            return COLORS["warning"]
        return COLORS["accent"] if source == "primary_5h" else COLORS["accent_alt"]

    def poll(self):
        if self.closing:
            return
        try:
            while True:
                payload = self.queue.get_nowait()
                if payload.get("_channel_done"):
                    channel = payload["_channel_done"]
                    self.application_controller.finish(channel, payload.get("_generation"))
                    if channel == "quota":
                        if not self.closing:
                            self.after(self.application_controller.quota_delay_ms, self.refresh)
                    elif channel == "activity" and not self.closing:
                        self.after(1000, self.refresh_activity)
                    continue
                channel = payload.get("_channel")
                if channel and not self.application_controller.is_current(channel, payload.get("_generation")):
                    continue
                if channel == "activity":
                    self.latest_activity = payload.get("_activity", self.latest_activity)
                elif channel == "quota":
                    if "error" in payload:
                        self.quota_state.fail("transport_error")
                        if self.quota_state.last_good is not None:
                            self.latest_quota = self.quota_state.last_good
                        self.render_status()
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
        if not self.lifecycle.begin_close():
            return
        if hasattr(self, "application_controller"):
            self.application_controller.shutdown()
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
        notify_existing_instance()
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
