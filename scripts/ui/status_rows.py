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
        self.progress_tracks = {}
        self.progress_fills = {}
        self._main_hud_layout = False
        self._visible_ids = ()
        self.bind("<Map>", lambda _event: (self._layout_quota_marker(), self._layout_main_quota_bars(self._visible_ids)), add="+")
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
                pady=0,
            )
            self.labels[row_id] = label
            if row_id in {"primary_5h", "weekly"}:
                track = tk.Frame(
                    self,
                    bg=COLORS["surface_alt"],
                    height=3,
                    highlightthickness=1,
                    highlightbackground=COLORS["text"],
                    highlightcolor=COLORS["text"],
                )
                fill = tk.Frame(track, bg=COLORS["accent"], height=1)
                self.progress_tracks[row_id] = track
                self.progress_fills[row_id] = fill
        self.set_visible_rows({})
        self.configure_rows(text=text)

    @property
    def event_widgets(self):
        return (
            self,
            *self.labels.values(),
            *self.progress_tracks.values(),
            *self.progress_fills.values(),
            self.quota_label,
        )

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
        if self._main_hud_layout:
            self.quota_label.place_forget()
            return
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
        main_hud = bool(settings.get("_main_hud_layout"))
        self._main_hud_layout = main_hud
        visible = {
            "activity": not main_hud,
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
        for track in self.progress_tracks.values():
            track.place_forget()
        visible_ids = [row_id for row_id in ROW_IDS if visible[row_id]]
        self._visible_ids = tuple(visible_ids)
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
        if main_hud:
            self.quota_divider.place_forget()
            self.quota_label.place_forget()
            self._layout_main_quota_bars(visible_ids)
        self.quota_divider.lift()
        self.quota_label.lift()
        self.update_idletasks()

    def _layout_main_quota_bars(self, visible_ids):
        if not self._main_hud_layout:
            return
        if not self.winfo_width() or not self.winfo_height():
            return
        row_count = max(1, len(visible_ids))
        for row_id, track in self.progress_tracks.items():
            if row_id not in visible_ids:
                continue
            label = self.labels[row_id]
            bar_y = label.winfo_y() + max(1, round(label.winfo_height() * 0.72))
            track.place(
                relx=0.46,
                y=bar_y,
                relwidth=0.38,
                height=max(2, round(label.winfo_height() * 0.1)),
                anchor="nw",
            )
            self.progress_fills[row_id].place(x=0, y=0, relheight=1, anchor="nw")
            track.lift()
            self.progress_fills[row_id].lift()

    def layout_progress_bars(self):
        """Reflow quota bars after the parent receives its final geometry."""
        self._layout_main_quota_bars(self._visible_ids)

    def set_quota_progress(self, remaining, colors=None):
        remaining = remaining if isinstance(remaining, dict) else {}
        colors = colors if isinstance(colors, dict) else {}
        for row_id, fill in self.progress_fills.items():
            value = remaining.get(row_id)
            ratio = 0.0 if value is None else max(0.0, min(1.0, float(value) / 100.0))
            fill.configure(bg=colors.get(row_id, COLORS["accent"]))
            fill.place_configure(relwidth=ratio)

    def row_values(self):
        return {row_id: label.cget("text") for row_id, label in self.labels.items()}
