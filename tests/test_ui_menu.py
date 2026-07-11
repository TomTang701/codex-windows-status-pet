import runpy
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))


class DummyServer:
    def __init__(self, _queue):
        self.proc = None

    def stop(self):
        pass


class DummyTray:
    def __init__(self, _actions):
        pass

    def stop(self):
        pass


class MenuInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "codex_status_pet.py"))
        cls.module["AppServer"] = DummyServer
        cls.module["TrayIcon3"] = DummyTray

    @staticmethod
    def menu_items(popup):
        body = popup.winfo_children()[0]
        return [
            child for child in body.winfo_children()
            if child.winfo_class() in {"Button", "Checkbutton"}
        ]

    def test_popup_contains_only_the_five_approved_actions(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            labels = [item.cget("text") for item in self.menu_items(app.context_menu)]
            self.assertEqual(labels, ["显示设置", "置顶", "锁定位置", "隐藏窗口", "退出"])
            for removed in ("立即刷新", "复制诊断摘要", "恢复上次设置"):
                self.assertNotIn(removed, labels)
        finally:
            app.destroy()

    def test_settings_button_is_invokable_once_from_popup(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            popup = app.context_menu
            settings = next(item for item in self.menu_items(popup) if item.cget("text") == "显示设置")
            settings.invoke()
            app.update_idletasks()
            self.assertIsNotNone(app.settings_dialog)
            self.assertGreaterEqual(app.settings_dialog.winfo_x(), 0)
            self.assertGreaterEqual(app.settings_dialog.winfo_y(), 0)
            self.assertFalse(popup.winfo_exists())
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            app.destroy()

    def test_hide_button_dispatches_once_and_closes(self):
        app = self.module["Pet"]()
        calls = []
        app.hide_window = lambda: calls.append("hide")
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            popup = app.context_menu
            hide = next(item for item in self.menu_items(popup) if item.cget("text") == "隐藏窗口")
            hide.invoke()
            app.update_idletasks()
            self.assertEqual(calls, ["hide"])
            self.assertFalse(popup.winfo_exists())
        finally:
            app.destroy()

    def test_escape_closes_popup_and_releases_owner_reference(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            popup = app.context_menu
            popup.event_generate("<Escape>")
            app.update()
            self.assertIsNone(app.context_menu)
            self.assertFalse(popup.winfo_exists())
        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
