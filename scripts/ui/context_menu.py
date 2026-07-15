"""First-click-safe context menu adapter for the status overlay."""

from __future__ import annotations

import logging
import tkinter as tk

try:
    from api.display_api import place_popup, work_area_for_point
    from api.menu_model_api import build_menu_items
    from api.runtime_api import ensure_overlay_toolwindow
    from ui.theme import COLORS, FONT_FAMILY
except ModuleNotFoundError:
    from scripts.api.display_api import place_popup, work_area_for_point
    from scripts.api.menu_model_api import build_menu_items
    from scripts.api.runtime_api import ensure_overlay_toolwindow
    from scripts.ui.theme import COLORS, FONT_FAMILY


def show_context_menu(owner, event):
    """Show and own the popup menu for a Pet-like owner object."""
    def refresh_shell(widget):
        try:
            if widget.winfo_exists():
                ensure_overlay_toolwindow(widget.winfo_id())
        except tk.TclError:
            pass

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
    refresh_shell(popup)
    popup.configure(bg=COLORS["border"])
    popup.geometry(f"+{event.x_root}+{event.y_root}")

    def close_popup():
        if getattr(owner, "context_menu", None) is popup:
            owner.context_menu = None
        try:
            popup.grab_release()
            popup.destroy()
        except tk.TclError:
            pass
        refresh_shell(owner)

    def run_and_close(command):
        close_popup()
        try:
            command()
            refresh_shell(owner)
        except Exception:
            logging.getLogger("codex-status-pet").exception("context-menu command failed")

    body = tk.Frame(popup, bg=COLORS["surface"], bd=1, relief="solid")
    body.pack(padx=1, pady=1)
    tk.Label(
        body,
        text="CODEX",
        bg=COLORS["surface"],
        fg=COLORS["accent"],
        anchor="w",
        font=(FONT_FAMILY, 8, "bold"),
    ).pack(fill="x", padx=10, pady=(7, 3))
    tk.Frame(body, height=1, bg=COLORS["border"]).pack(fill="x", padx=6, pady=(0, 3))
    button_options = {
        "anchor": "w", "width": 22, "bd": 0, "relief": "flat",
        "bg": COLORS["surface"], "fg": COLORS["text"],
        "activebackground": COLORS["surface_alt"],
        "activeforeground": COLORS["accent"],
        "font": (FONT_FAMILY, 10), "padx": 10, "pady": 5,
        "cursor": "hand2",
        "highlightthickness": 1,
        "highlightbackground": COLORS["surface"],
        "highlightcolor": COLORS["accent"],
    }
    commands = {
        "settings": owner.show_settings,
        "topmost": owner.toggle_topmost,
        "lock": owner.toggle_locked,
        "compact": lambda: owner.set_manual_compact(owner.compact_var.get()),
        "hide": owner.hide_window,
        "exit": owner.close,
    }
    variables = {
        "topmost": owner.topmost_var,
        "lock": owner.locked_var,
        "compact": owner.compact_var,
    }
    items = build_menu_items(
        owner.settings["language"], visible=True,
        topmost=owner.settings["topmost"], locked=owner.settings["locked"],
        compact=owner.settings["compact"],
    )

    def set_item_active(widget, active):
        widget.configure(
            bg=COLORS["surface_alt"] if active else COLORS["surface"],
            fg=COLORS["accent"] if active else COLORS["text"],
            highlightbackground=COLORS["accent"] if active else COLORS["surface"],
        )

    def toggle_and_run(action):
        variables[action].set(not variables[action].get())
        run_and_close(commands[action])

    menu_widgets = []
    for item in items:
        if item.action == "exit":
            tk.Frame(body, height=1, bg=COLORS["border"]).pack(fill="x", padx=2, pady=3)
        if item.checked is None:
            widget = tk.Button(
                body, text=item.label,
                command=lambda command=commands[item.action]: run_and_close(command),
                **button_options,
            )
        else:
            state_mark = "✓" if item.checked else "○"
            widget = tk.Button(
                body,
                text=f"{item.label}  {state_mark}",
                command=lambda action=item.action: toggle_and_run(action),
                **button_options,
            )
        widget.bind("<Enter>", lambda _event, widget=widget: set_item_active(widget, True), add="+")
        widget.bind("<Leave>", lambda _event, widget=widget: set_item_active(widget, False), add="+")
        widget.bind("<FocusIn>", lambda _event, widget=widget: set_item_active(widget, True), add="+")
        widget.bind("<FocusOut>", lambda _event, widget=widget: set_item_active(widget, False), add="+")
        widget.pack(fill="x", padx=2, pady=1)
        menu_widgets.append(widget)
    if menu_widgets:
        menu_widgets[0].focus_set()
        set_item_active(menu_widgets[0], True)
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
