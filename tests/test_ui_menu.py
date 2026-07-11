import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

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

    def test_routine_pet_save_preserves_protected_configuration(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                app.settings_path.write_text("{damaged", encoding="utf-8")
                app.settings["x"] = 4151
                self.assertFalse(app.save_settings())
                self.assertEqual(app.settings_path.read_text(encoding="utf-8"), "{damaged")
        finally:
            app.destroy()

    def test_restore_defaults_then_save_explicitly_replaces_protected_configuration(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                app.settings_path.write_text("{damaged", encoding="utf-8")
                app.show_settings()
                app.update_idletasks()
                body = app.settings_dialog.winfo_children()[0]
                button_row = body.grid_slaves(row=8)[0]
                buttons = {child.cget("text"): child for child in button_row.winfo_children()}
                buttons["恢复默认值"].invoke()
                buttons["保存"].invoke()
                app.update_idletasks()
                result = app.settings_path.read_text(encoding="utf-8")
                self.assertIn('"schema_version": 1', result)
                self.assertNotEqual(result, "{damaged")
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            app.destroy()

    def test_rejected_ordinary_save_keeps_dialog_open_and_source_unchanged(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                app.settings_path.write_text("{damaged", encoding="utf-8")
                app.show_settings()
                app.update_idletasks()
                dialog = app.settings_dialog
                body = dialog.winfo_children()[0]
                button_row = body.grid_slaves(row=8)[0]
                buttons = {child.cget("text"): child for child in button_row.winfo_children()}
                with mock.patch("ui.settings_dialog.messagebox.showwarning") as warning:
                    buttons["保存"].invoke()
                self.assertTrue(dialog.winfo_exists())
                self.assertEqual(app.settings_path.read_text(encoding="utf-8"), "{damaged")
                warning.assert_called_once()
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            app.destroy()


if __name__ == "__main__":
    unittest.main()
