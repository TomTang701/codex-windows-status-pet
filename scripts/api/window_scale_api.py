"""Pure proportional window and typography scale calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass


BASE_WINDOW_WIDTH = 330
BASE_WINDOW_HEIGHT = 138
BASE_TEXT_FONT_SIZE = 10
BASE_FACE_FONT_SIZE = 28
BASE_HORIZONTAL_PADDING = 12
BASE_VERTICAL_PADDING = 10
BASE_FACE_TEXT_GAP = 5
BASE_WRAPLENGTH = 260
MIN_WINDOW_SCALE_PERCENT = 80
MAX_WINDOW_SCALE_PERCENT = 200
WINDOW_SCALE_STEP = 5
DEFAULT_WINDOW_SCALE_PERCENT = 100


@dataclass(frozen=True)
class WindowMetrics:
    """One coherent expanded-window metric set derived from one percentage."""

    scale_percent: int
    width: int
    height: int
    text_font_size: int
    face_font_size: int
    horizontal_padding: int
    vertical_padding: int
    face_text_gap: int
    wraplength: int


def _finite_number(value, default):
    if isinstance(value, bool):
        return float(default)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return float(default)
    return number if math.isfinite(number) else float(default)


def clamp_scale_percent(value) -> float:
    """Return a finite percentage inside the supported range."""
    number = _finite_number(value, DEFAULT_WINDOW_SCALE_PERCENT)
    return min(MAX_WINDOW_SCALE_PERCENT, max(MIN_WINDOW_SCALE_PERCENT, number))


def quantize_scale_percent(value) -> int:
    """Clamp and select the nearest supported step with half-up ties."""
    clamped = clamp_scale_percent(value)
    stepped = math.floor((clamped + WINDOW_SCALE_STEP / 2) / WINDOW_SCALE_STEP) * WINDOW_SCALE_STEP
    return int(min(MAX_WINDOW_SCALE_PERCENT, max(MIN_WINDOW_SCALE_PERCENT, stepped)))


def derive_window_metrics(value) -> WindowMetrics:
    """Derive expanded geometry, typography, wrapping, and spacing once."""
    percent = quantize_scale_percent(value)
    scale = percent / 100
    return WindowMetrics(
        scale_percent=percent,
        width=round(BASE_WINDOW_WIDTH * scale),
        height=math.ceil(BASE_WINDOW_HEIGHT * scale),
        text_font_size=round(BASE_TEXT_FONT_SIZE * scale),
        face_font_size=round(BASE_FACE_FONT_SIZE * scale),
        horizontal_padding=round(BASE_HORIZONTAL_PADDING * scale),
        vertical_padding=round(BASE_VERTICAL_PADDING * scale),
        face_text_gap=round(BASE_FACE_TEXT_GAP * scale),
        wraplength=round(BASE_WRAPLENGTH * scale),
    )


def infer_scale_percent(width, height) -> int:
    """Infer one deterministic scale from legacy visual area."""
    width_value = _finite_number(width, -1)
    height_value = _finite_number(height, -1)
    if width_value <= 0 or height_value <= 0:
        return DEFAULT_WINDOW_SCALE_PERCENT
    area_ratio = (width_value * height_value) / (BASE_WINDOW_WIDTH * BASE_WINDOW_HEIGHT)
    return quantize_scale_percent(math.sqrt(area_ratio) * 100)
