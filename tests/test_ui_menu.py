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

    def test_settings_button_is_invokable_once_from_popup(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            popup = app.context_menu
            body = popup.winfo_children()[0]
            buttons = [child for child in body.winfo_children() if child.winfo_class() == "Button"]
            self.assertGreaterEqual(len(buttons), 2)
            buttons[1].invoke()
            app.update_idletasks()
            self.assertIsNotNone(app.settings_dialog)
            self.assertGreaterEqual(app.settings_dialog.winfo_x(), 0)
            self.assertGreaterEqual(app.settings_dialog.winfo_y(), 0)
            self.assertFalse(popup.winfo_exists())
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            app.destroy()


if __name__ == "__main__":
    unittest.main()
