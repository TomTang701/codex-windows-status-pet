"""First-click-safe context menu adapter for the status overlay."""

from __future__ import annotations

import logging
import tkinter as tk

try:
    from api.display_api import place_popup, work_area_for_point
    from api.localization_api import translate
except ModuleNotFoundError:
    from scripts.api.display_api import place_popup, work_area_for_point
    from scripts.api.localization_api import translate


def show_context_menu(owner, event):
    """Show and own the popup menu for a Pet-like owner object."""
    if owner.compact:
        owner.set_compact(False)
    old_menu = getattr(owner, "context_menu", None)
    if old_menu is not None:
        try:
            old_menu.grab_release()
            old_menu.destroy()
        except tk.TclError:
            pass

    popup = tk.Toplevel(owner)
    owner.context_menu = popup
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.configure(bg="#e5e7eb")
    popup.geometry(f"+{event.x_root}+{event.y_root}")

    def close_popup():
        if getattr(owner, "context_menu", None) is popup:
            owner.context_menu = None
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
    button_options = {
        "anchor": "w", "width": 18, "bd": 0, "relief": "flat",
        "bg": "#f3f4f6", "activebackground": "#dbeafe",
    }
    language = owner.settings["language"]
    tk.Button(body, text=translate(language, "settings"), command=lambda: run_and_close(owner.show_settings), **button_options).pack(fill="x", padx=2, pady=1)
    tk.Checkbutton(body, text=translate(language, "always_on_top"), variable=owner.topmost_var, command=lambda: run_and_close(owner.toggle_topmost), **button_options).pack(fill="x", padx=2, pady=1)
    tk.Checkbutton(body, text=translate(language, "lock_position"), variable=owner.locked_var, command=lambda: run_and_close(owner.toggle_locked), **button_options).pack(fill="x", padx=2, pady=1)
    tk.Frame(body, height=1, bg="#d1d5db").pack(fill="x", padx=2, pady=3)
    tk.Button(body, text=translate(language, "hide_window"), command=lambda: run_and_close(owner.hide_window), **button_options).pack(fill="x", padx=2, pady=1)
    tk.Button(body, text=translate(language, "exit"), command=lambda: run_and_close(owner.close), **button_options).pack(fill="x", padx=2, pady=1)
    popup.bind("<Escape>", lambda _event: (close_popup(), "break")[1])
    popup.bind("<Button-3>", lambda _event: close_popup())
    popup.bind("<FocusOut>", lambda _event: popup.after_idle(close_popup))
    popup.update_idletasks()
    work_area = work_area_for_point(event.x_root, event.y_root)
    popup_x, popup_y = place_popup(
        event.x_root, event.y_root, popup.winfo_reqwidth(), popup.winfo_reqheight(), work_area
    )
    popup.geometry(f"+{popup_x}+{popup_y}")
    popup.grab_set()
    popup.focus_force()
