"""Notification-area icon adapter; application state remains in the owner queue."""

from __future__ import annotations

import logging
import threading

from PIL import Image, ImageDraw
import pystray

try:
    from api.localization_api import translate
except ModuleNotFoundError:
    from scripts.api.localization_api import translate


def tray_menu_labels(language):
    """Return visible tray labels without changing stable queue action IDs."""
    return tuple(
        translate(language, key)
        for key in ("show_window", "hide_window", "open_settings", "exit")
    )


class TrayIcon3:
    """Stable notification-area integration backed by pystray."""

    def __init__(self, actions, language="en"):
        self.actions = actions
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
        show, hide, settings, exit_label = tray_menu_labels(language)
        return pystray.Menu(
            pystray.MenuItem(show, lambda icon, item: actions.put("show")),
            pystray.MenuItem(hide, lambda icon, item: actions.put("hide")),
            pystray.MenuItem(settings, lambda icon, item: actions.put("settings")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(exit_label, lambda icon, item: actions.put("exit")),
        )

    def set_language(self, language):
        """Replace only visible menu labels; keep this tray owner and thread."""
        self.language = language
        self.icon.menu = self._menu(language)

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
