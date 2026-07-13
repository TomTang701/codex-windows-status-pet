"""Tk-independent semantic model shared by overlay and tray menus."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from api.localization_api import translate
except ModuleNotFoundError:
    from scripts.api.localization_api import translate


@dataclass(frozen=True)
class MenuItem:
    action: str
    label: str
    checked: bool | None = None


def build_menu_items(language, *, visible, topmost, locked, compact):
    """Return the one product menu contract for a live application state."""
    visibility_action = "hide" if visible else "show"
    visibility_key = "hide_window" if visible else "show_window"
    return (
        MenuItem("settings", translate(language, "settings")),
        MenuItem("topmost", translate(language, "always_on_top"), bool(topmost)),
        MenuItem("lock", translate(language, "lock_position"), bool(locked)),
        MenuItem("compact", translate(language, "compact"), bool(compact)),
        MenuItem(visibility_action, translate(language, visibility_key)),
        MenuItem("exit", translate(language, "exit")),
    )
