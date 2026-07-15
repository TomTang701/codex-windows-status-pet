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

    def __init__(self, owner, *, text, font, fg, bg, wraplength, quota_label="QUOTA"):
        super().__init__(owner, bg=bg)
        self.quota_divider = tk.Frame(self, bg=COLORS["border"], height=1)
        self.quota_label = tk.Label(
            self,
            text=quota_label,
            bg=bg,
            fg=COLORS["muted"],
            font=(FONT_FAMILY, 6, "bold"),
            padx=4,
            pady=0,
        )
        self.labels = {}
        self.bind("<Map>", lambda _event: self._layout_quota_marker(), add="+")
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
        return (self, *self.labels.values(), self.quota_label)

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
        if font is not None:
            for row_id, label in self.labels.items():
                label.configure(font=self._font_for_row(font, row_id))
            self.quota_label.configure(font=self._marker_font(font))
            options.pop("font", None)
        if bg is not None:
            tk.Frame.configure(self, bg=bg)
            self.quota_label.configure(bg=bg)
        if options:
            for label in self.labels.values():
                label.configure(**options)

    def set_quota_label(self, value):
        self.quota_label.configure(text=value)

    def _layout_quota_marker(self):
        visible_ids = [
            row_id
            for row_id, label in self.labels.items()
            if label.winfo_manager() in {"pack", "place"}
        ]
        if len(visible_ids) < 3:
            self.quota_label.place_forget()
            return
        self.quota_label.place(relx=0.5, rely=2 / len(visible_ids), anchor="center")

    @staticmethod
    def _font_for_row(font, row_id):
        if row_id != "activity" or not isinstance(font, (tuple, list)):
            return font
        return (*font, "bold")

    @staticmethod
    def _marker_font(font):
        if isinstance(font, (tuple, list)) and len(font) >= 2:
            try:
                size = max(1, round(abs(int(font[1])) * 0.6))
                return (font[0], -size, "bold")
            except (TypeError, ValueError):
                pass
        return (FONT_FAMILY, 6, "bold")

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
            label.grid_forget()
            label.place_forget()
        self.quota_divider.place_forget()
        self.quota_label.place_forget()
        visible_ids = [row_id for row_id in ROW_IDS if visible[row_id]]
        visible_count = len(visible_ids)
        if not self.winfo_ismapped():
            for row_id in visible_ids:
                self.labels[row_id].pack(fill="x", expand=True, anchor="w")
            self._layout_quota_marker()
            return
        for visible_index, row_id in enumerate(visible_ids):
            label = self.labels[row_id]
            label.place(
                relx=0,
                rely=visible_index / visible_count,
                relwidth=1,
                relheight=1 / visible_count,
                anchor="nw",
            )
        self.quota_divider.place(
            relx=0,
            rely=2 / visible_count,
            relwidth=1,
            y=-1,
            height=1,
            anchor="nw",
        )
        self._layout_quota_marker()
        self.quota_divider.lift()
        self.quota_label.lift()
        self.update_idletasks()

    def row_values(self):
        return {row_id: label.cget("text") for row_id, label in self.labels.items()}
