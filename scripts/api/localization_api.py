"""Static, Tk-independent text for the supported runtime languages."""

from __future__ import annotations


SUPPORTED_LANGUAGES = ("en", "zh-CN")

_TEXT = {
    "en": {
        "idle": "Idle",
        "activity": "Codex {detail}",
    },
    "zh-CN": {
        "idle": "空闲",
        "activity": "Codex {detail}",
    },
}


def normalize_language(value):
    """Return a supported code and an optional normalization warning."""
    if value in SUPPORTED_LANGUAGES:
        return value, None
    if value is None:
        return "en", None
    return "en", "language is invalid; English retained"


def translate(language, key, **format_values):
    """Return one translated user-facing string or fail visibly for a bad key."""
    normalized, _warning = normalize_language(language)
    return _TEXT[normalized][key].format(**format_values)
