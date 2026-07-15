"""Tk adapter for independently rendered overlay status rows."""

from __future__ import annotations

import tkinter as tk

try:
    from ui.theme import COLORS, FONT_FAMILY
except ModuleNotFoundError:
    from scripts.ui.theme import COLORS, FONT_FAMILY

try:
    from api.status_rows_api import ROW_IDS, split_status_text
except ModuleNotFoundError:
    from scripts.api.status_rows_api import ROW_IDS, split_status_text


class StatusRows(tk.Frame):
    """Five persistent single-line labels with stable row identities."""

    def __init__(self, owner, *, text, font, fg, bg, wraplength):
        super().__init__(owner, bg=bg)
        self.labels = {}
        for row_id in ROW_IDS:
            label = tk.Label(
                self,
                text="",
                justify="left",
                anchor="w",
                font=font,
                fg=fg,
                bg=bg,
                wraplength=wraplength,
                padx=2,
            )
            self.labels[row_id] = label
        self.set_visible_rows({})
        self.configure_rows(text=text)

    @property
    def event_widgets(self):
        return (self, *self.labels.values())

    def configure_rows(self, *, rows=None, text=None, fg=None, bg=None, font=None, wraplength=None):
        if text is not None:
            rows = split_status_text(text).as_dict()
        if rows is not None:
            for row_id, value in rows.items():
                if row_id in self.labels:
                    self.labels[row_id].configure(text=str(value))
        options = {
            key: value
            for key, value in {"fg": fg, "bg": bg, "font": font, "wraplength": wraplength}.items()
            if value is not None
        }
        if bg is not None:
            tk.Frame.configure(self, bg=bg)
        if options:
            for label in self.labels.values():
                label.configure(**options)

    def set_visible_rows(self, settings):
        visible = {
            "activity": True,
            "progress": True,
            "primary_5h": bool(settings.get("show_primary_5h", True)),
            "weekly": bool(settings.get("show_weekly", True)),
            "reset_credit": bool(settings.get("show_reset_credit", True)),
        }
        for label in self.labels.values():
            label.pack_forget()
        for row_id in ROW_IDS:
            if visible[row_id]:
                self.labels[row_id].pack(fill="x", expand=True, anchor="w")

    def row_values(self):
        return {row_id: label.cget("text") for row_id, label in self.labels.items()}
