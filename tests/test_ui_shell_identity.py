"""Win32 Shell identity contract for the real Tk overlay root HWND."""

from __future__ import annotations

import ctypes
import gc
import json
import runpy
import tempfile
import time
import unittest
from pathlib import Path

from tests import runtime_geometry_transition_probe
from tests.runtime_geometry_transition_probe import CONFIG, DummyServer, DummyTray, ROOT


WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
GWL_EXSTYLE = -20
GA_ROOT = 2


def root_hwnd(widget_hwnd):
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetAncestor.argtypes = (ctypes.c_void_p, ctypes.c_uint)
    user32.GetAncestor.restype = ctypes.c_void_p
    return int(user32.GetAncestor(widget_hwnd, GA_ROOT))


def extended_style(hwnd):
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetWindowLongPtrW.argtypes = (ctypes.c_void_p, ctypes.c_int)
    user32.GetWindowLongPtrW.restype = ctypes.c_longlong
    return int(user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE))


class ShellIdentityTests(unittest.TestCase):
    def assert_shell_identity(self, app):
        hwnd = root_hwnd(app.winfo_id())
        self.assertNotEqual(hwnd, 0)
        style = extended_style(hwnd)
        self.assertTrue(
            style & WS_EX_TOOLWINDOW,
            f"overlay root HWND {hwnd} lost WS_EX_TOOLWINDOW",
        )
        self.assertFalse(
            style & WS_EX_APPWINDOW,
            f"overlay root HWND {hwnd} gained WS_EX_APPWINDOW",
        )

    def create_app(self, home):
        config_path = home / ".codex" / "codex-windows-status-pet.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps(CONFIG), encoding="utf-8")
        module = runpy.run_path(str(ROOT / "scripts" / "codex_status_pet.py"))
        module["AppServer"] = DummyServer
        module["TrayIcon3"] = DummyTray
        return module["Pet"]()

    def destroy_app(self, app):
        app.application_controller.shutdown()
        for callback in app.tk.call("after", "info"):
            try:
                app.after_cancel(callback)
            except Exception:
                pass
        app.topmost_var = None
        app.locked_var = None
        app.destroy()
        gc.collect()

    def test_visible_overlay_root_has_toolwindow_shell_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                app = self.create_app(home)
                app.update_idletasks()
                app.update()
                self.assert_shell_identity(app)
            finally:
                if app is not None:
                    self.destroy_app(app)
                Path.home = original_home

    def test_shell_identity_survives_required_lifecycle_transitions(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                app = self.create_app(home)
                app.update()
                self.assert_shell_identity(app)

                settings = dict(app.settings)
                settings.update({"alpha": 0.55, "window_scale_percent": 150, "topmost": False})
                app.apply_settings(settings)
                app.update()
                self.assert_shell_identity(app)

                app.locked_var.set(False)
                app.toggle_locked()
                app.hide_window()
                app.show_window()
                app.set_compact(True)
                app.set_compact(False)
                app.update()
                self.assert_shell_identity(app)
            finally:
                if app is not None:
                    self.destroy_app(app)
                Path.home = original_home

    def test_settings_dialog_is_not_an_ordinary_taskbar_window(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                app = self.create_app(home)
                app.show_settings()
                app.update_idletasks()
                self.assert_shell_identity(app.settings_dialog)
            finally:
                if app is not None:
                    self.destroy_app(app)
                Path.home = original_home

    def test_overlay_keeps_toolwindow_identity_after_settings_close_settles(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            original_home = Path.home
            Path.home = classmethod(lambda cls: home)
            app = None
            try:
                app = self.create_app(home)
                app.show_settings()
                app.update_idletasks()
                app.close_settings(app.settings_dialog)
                deadline = time.monotonic() + 0.35
                while time.monotonic() < deadline:
                    app.update()
                    time.sleep(0.01)
                self.assert_shell_identity(app)
            finally:
                if app is not None:
                    self.destroy_app(app)
                Path.home = original_home

    def test_overlay_keeps_toolwindow_identity_after_each_settings_close_path(self):
        def buttons(widget):
            result = []
            for child in widget.winfo_children():
                result.extend(buttons(child))
                if child.winfo_class() == "Button":
                    result.append(child)
            return result

        for close_action in ("Close", "Save"):
            with tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                original_home = Path.home
                Path.home = classmethod(lambda cls: home)
                app = None
                try:
                    app = self.create_app(home)
                    app.show_settings()
                    app.update_idletasks()
                    button = next(button for button in buttons(app.settings_dialog) if button.cget("text") == close_action)
                    button.invoke()
                    deadline = time.monotonic() + 0.35
                    while time.monotonic() < deadline:
                        app.update()
                        time.sleep(0.01)
                    self.assert_shell_identity(app)
                finally:
                    if app is not None:
                        self.destroy_app(app)
                    Path.home = original_home

    def test_shell_identity_survives_full_runtime_transition_probe(self):
        self.assertEqual(runtime_geometry_transition_probe.main(), 0)
        output_path = ROOT / ".build" / "v051-runtime-transition-probe.json"
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertTrue(payload["records"])
        for record in payload["records"]:
            identity = record["shell_identity"]
            self.assertTrue(
                identity["toolwindow"],
                f"{record['transition']} / {record['stage']} lost WS_EX_TOOLWINDOW",
            )
            self.assertFalse(
                identity["appwindow"],
                f"{record['transition']} / {record['stage']} gained WS_EX_APPWINDOW",
            )


if __name__ == "__main__":
    unittest.main()
