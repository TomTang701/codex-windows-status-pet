"""Reversible percentage-based resize session."""

from __future__ import annotations


class ResizeSession:
    def __init__(self, width, height, width_bounds=(180, 1200), height_bounds=(80, 800)):
        self.base_width = int(width)
        self.base_height = int(height)
        self.width_bounds = width_bounds
        self.height_bounds = height_bounds
        self.scale_percent = 100

    def set_scale(self, percent):
        self.scale_percent = max(50, min(200, int(percent)))

    def step(self, delta_percent):
        self.set_scale(self.scale_percent + int(delta_percent))
        return self.dimensions()

    def dimensions(self):
        width = round(self.base_width * self.scale_percent / 100)
        height = round(self.base_height * self.scale_percent / 100)
        return (
            min(self.width_bounds[1], max(self.width_bounds[0], width)),
            min(self.height_bounds[1], max(self.height_bounds[0], height)),
        )
