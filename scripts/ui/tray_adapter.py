"""Notification-area icon adapter; application state remains in the owner queue."""

from __future__ import annotations

import logging
import threading

from PIL import Image, ImageDraw
import pystray

try:
    from api.menu_model_api import build_menu_items
except ModuleNotFoundError:
    from scripts.api.menu_model_api import build_menu_items


def tray_menu_items(language, *, visible, topmost, locked, compact):
    """Expose the shared semantic model for tray-only tests and adapters."""
    return build_menu_items(
        language, visible=visible, topmost=topmost, locked=locked, compact=compact
    )


class TrayIcon3:
    """Stable notification-area integration backed by pystray."""

    def __init__(self, actions, language="en", *, visible=True, topmost=True, locked=False, compact=False):
        self.actions = actions
        self._menu_state = {
            "visible": bool(visible), "topmost": bool(topmost),
            "locked": bool(locked), "compact": bool(compact),
        }
        image = Image.new("RGBA", (64, 64), (17, 24, 39, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((12, 12, 52, 52), fill=(147, 197, 253, 255))
        draw.ellipse((22, 18, 30, 26), fill=(17, 24, 39, 255))
        draw.ellipse((34, 18, 42, 26), fill=(17, 24, 39, 255))
        self.icon = pystray.Icon("codex-windows-status-pet", image, "Codex Status Pet")
        self.set_language(language)
        self._stopped = False
        self.thread = threading.Thread(target=self._run, name="codex-tray", daemon=True)
        self.thread.start()

    def _menu(self, language):
        entries = tray_menu_items(language, **getattr(self, "_menu_state", {
            "visible": True, "topmost": True, "locked": False, "compact": False,
        }))
        def queue_action(action):
            def callback(_icon, _item):
                self.actions.put(action)
            return callback

        widgets = []
        for entry in entries:
            if entry.action == "exit":
                widgets.append(pystray.Menu.SEPARATOR)
            widgets.append(pystray.MenuItem(
                entry.label,
                queue_action(entry.action),
                checked=(lambda _item, checked=entry.checked: bool(checked))
                if entry.checked is not None else None,
            ))
        return pystray.Menu(*widgets)

    def set_language(self, language):
        """Replace only visible menu labels; keep this tray owner and thread."""
        self.language = language
        self.icon.menu = self._menu(language)

    def set_menu_state(self, language, *, visible, topmost, locked, compact):
        """Receive a Tk-owned immutable state snapshot; never inspect Tk here."""
        self._menu_state = {
            "visible": bool(visible), "topmost": bool(topmost),
            "locked": bool(locked), "compact": bool(compact),
        }
        self.set_language(language)

    def _run(self):
        try:
            self.icon.run()
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon failed")
            self.actions.put("tray_error")

    def stop(self):
        if self._stopped:
            return
        self._stopped = True
        try:
            self.icon.stop()
        except Exception:
            logging.getLogger("codex-status-pet").exception("notification-area icon shutdown failed")
