"""Tk adapter for independently rendered overlay status rows."""

from __future__ import annotations

import tkinter as tk

try:
    from api.status_rows_api import ROW_IDS, split_status_text
except ModuleNotFoundError:
    from scripts.api.status_rows_api import ROW_IDS, split_status_text


class StatusRows(tk.Frame):
    """Five stable single-line labels with a Label-compatible config surface."""

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
            )
            label.pack(fill="x", anchor="w")
            self.labels[row_id] = label
        self.configure_rows(text=text)

    @property
    def event_widgets(self):
        return (self, *self.labels.values())

    def configure_rows(self, *, text=None, fg=None, bg=None, font=None, wraplength=None):
        if text is not None:
            rows = split_status_text(text).as_dict()
            for row_id, value in rows.items():
                self.labels[row_id].configure(text=value)
        options = {key: value for key, value in {
            "fg": fg, "bg": bg, "font": font, "wraplength": wraplength,
        }.items() if value is not None}
        if bg is not None:
            super().configure(bg=bg)
        if options:
            for label in self.labels.values():
                label.configure(**options)

    def config(self, cnf=None, **kwargs):
        if cnf:
            kwargs.update(cnf)
        self.configure_rows(**kwargs)

    configure = config
