"""Notification-area icon adapter; application state remains in the owner queue."""

from __future__ import annotations

import logging
import threading

from PIL import Image, ImageDraw
import pystray


class TrayIcon3:
    """Stable notification-area integration backed by pystray."""

    def __init__(self, actions):
        self.actions = actions
        image = Image.new("RGBA", (64, 64), (17, 24, 39, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((12, 12, 52, 52), fill=(147, 197, 253, 255))
        draw.ellipse((22, 18, 30, 26), fill=(17, 24, 39, 255))
        draw.ellipse((34, 18, 42, 26), fill=(17, 24, 39, 255))
        menu = pystray.Menu(
            pystray.MenuItem("显示窗口", lambda icon, item: actions.put("show")),
            pystray.MenuItem("隐藏窗口", lambda icon, item: actions.put("hide")),
            pystray.MenuItem("打开设置", lambda icon, item: actions.put("settings")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", lambda icon, item: actions.put("exit")),
        )
        self.icon = pystray.Icon("codex-windows-status-pet", image, "Codex Status Pet", menu)
        self._stopped = False
        self.thread = threading.Thread(target=self._run, name="codex-tray", daemon=True)
        self.thread.start()

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
