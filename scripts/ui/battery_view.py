"""Focused Tk view for the approved ten-cell 2×5 battery visual."""

from __future__ import annotations

import tkinter as tk


INACTIVE_COLOR = "#374151"
UNAVAILABLE_COLOR = "#6b7280"
STALE_COLOR = "#64748b"


class BatteryView(tk.Frame):
    """Persistent two-column, five-row battery cells ordered bottom-up."""

    def __init__(self, owner, *, bg, cell_size=2):
        super().__init__(owner, bg=bg)
        self.cells = []
        for index in range(10):
            cell = tk.Label(
                self, text="", width=cell_size, height=1, bd=1,
                relief="solid", bg=INACTIVE_COLOR,
            )
            cell.grid(row=4 - index // 2, column=index % 2, padx=1, pady=1)
            self.cells.append(cell)

    @property
    def event_widgets(self):
        return (self, *self.cells)

    def configure_presentation(self, presentation, *, stale=False, unavailable=False):
        available = bool(presentation.get("available"))
        for cell, state in zip(self.cells, presentation.get("segments", ())):
            color = UNAVAILABLE_COLOR if unavailable else STALE_COLOR if stale and available and state["lit"] else state["color"] if available and state["lit"] else (
                INACTIVE_COLOR if available else UNAVAILABLE_COLOR
            )
            cell.configure(bg=color)

    def set_compact(self, compact):
        """Scale the same ten cells down without changing their state or order."""
        if compact:
            options = {"width": 1, "height": 1, "font": ("Segoe UI", 1), "bd": 1}
            padding = {"padx": 0, "pady": 0}
        else:
            options = {"width": 2, "height": 1, "font": "TkDefaultFont", "bd": 1}
            padding = {"padx": 1, "pady": 1}
        for cell in self.cells:
            cell.configure(**options)
            cell.grid_configure(**padding)

    def set_metrics(self, text_font_size, compact=False):
        """Scale cell request geometry with the existing canonical window scale."""
        point_size = max(1, round(int(text_font_size) * (0.25 if compact else 0.45)))
        width = 1 if compact else max(1, round(int(text_font_size) / 5))
        padding = 0 if compact else 1
        for cell in self.cells:
            cell.configure(width=width, height=1, font=("Segoe UI", point_size))
            cell.grid_configure(padx=padding, pady=padding)
