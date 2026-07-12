import runpy
import sys
import tempfile
import unittest
import gc
import logging
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

    @staticmethod
    def descendants(widget):
        result = []
        for child in widget.winfo_children():
            result.append(child)
            result.extend(MenuInteractionTests.descendants(child))
        return result

    @staticmethod
    def destroy_app(app):
        """Stop callbacks/workers and collect Tk variables before destroying Tcl."""
        if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
            app.settings_dialog.destroy()
            app.settings_dialog = None
        if getattr(app, "refresh_controller", None) is not None:
            app.refresh_controller.shutdown()
        for callback in app.tk.call("after", "info"):
            try:
                app.after_cancel(callback)
            except Exception:
                pass
        app.topmost_var = None
        app.locked_var = None
        gc.collect()
        app.destroy()
        gc.collect()

    def test_popup_contains_only_the_five_approved_actions(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            labels = [item.cget("text") for item in self.menu_items(app.context_menu)]
            self.assertEqual(labels, ["显示设置", "置顶", "锁定位置", "隐藏窗口", "退出"])
            for removed in ("立即刷新", "复制诊断摘要", "恢复上次设置"):
                self.assertNotIn(removed, labels)
        finally:
            self.destroy_app(app)

    def test_tray_error_renders_rows_and_schedules_one_restart(self):
        app = self.module["Pet"]()
        try:
            app.tray_actions.put("tray_error")
            logger = logging.getLogger("codex-status-pet")
            with mock.patch.object(logger, "exception") as logged:
                app.process_tray_actions()
            logged.assert_not_called()
            self.assertEqual(app.text.row_values()["progress"], "托盘图标异常")
            self.assertEqual(
                app.text.labels["progress"].cget("fg"), "#fca5a5"
            )
            self.assertTrue(app.tray_restart_scheduled)
        finally:
            self.destroy_app(app)

    def test_render_status_uses_persisted_runtime_language(self):
        app = self.module["Pet"]()
        try:
            app.settings["language"] = "en"
            app.latest_activity = {"active": 0, "detail": "Idle", "progress": ""}
            app.latest_quota = {"rateLimits": {"primary": {}, "secondary": {"usedPercent": 45}}}
            app.render_status()
            self.assertEqual(app.text.row_values()["activity"], "Codex Idle")
            self.assertTrue(app.text.row_values()["weekly"].startswith("Week 55% /"))
        finally:
            self.destroy_app(app)

    def test_quota_transport_error_renders_unavailable_without_raw_exception(self):
        app = self.module["Pet"]()
        try:
            generation = app.application_controller.begin_quota()
            app.queue.put(
                {
                    "_channel": "quota",
                    "_generation": generation,
                    "error": "transport exploded",
                }
            )
            logger = logging.getLogger("codex-status-pet")
            with mock.patch.object(logger, "exception") as logged:
                app.poll()
            logged.assert_not_called()
            values = app.text.row_values()
            self.assertEqual(values["progress"], "额度暂不可用")
            self.assertNotIn("transport exploded", "\n".join(values.values()))
            self.assertEqual(app.quota_state.state, "unavailable")
        finally:
            self.destroy_app(app)

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
            self.destroy_app(app)

    def test_settings_dialog_has_two_existing_scales_and_one_discrete_source_scale(self):
        app = self.module["Pet"]()
        try:
            app.show_settings()
            app.update_idletasks()
            widgets = self.descendants(app.settings_dialog)
            scales = [widget for widget in widgets if widget.winfo_class() == "Scale"]
            texts = [widget.cget("text") for widget in widgets if "text" in widget.keys()]
            self.assertEqual(len(scales), 3)
            self.assertEqual(
                len([widget for widget in scales if float(widget.cget("to")) == 200.0]),
                1,
            )
            source_scale = next(
                widget
                for widget in scales
                if float(widget.cget("from")) == 0.0
                and float(widget.cget("to")) == 1.0
            )
            self.assertEqual(float(source_scale.cget("resolution")), 1.0)
            self.assertIn("透明度", texts)
            self.assertIn("窗口大小", texts)
            self.assertIn("电池显示内容", texts)
            self.assertIn("5小时", texts)
            self.assertIn("每周", texts)
            for removed in ("字体大小", "窗口大小 (宽, 高)", "−", "+", "等比例缩放"):
                self.assertNotIn(removed, texts)
            self.assertIn("默认位置 (X, Y)", texts)
            self.assertIn("刷新间隔 (秒)", texts)
            for retained in (
                "置顶", "锁定位置", "空闲时收缩", "字体颜色...", "背景颜色...",
                "保存", "应用", "恢复默认值", "关闭",
            ):
                self.assertIn(retained, texts)
        finally:
            self.destroy_app(app)

    def test_scale_slider_is_draft_only_until_apply_and_defaults_to_100(self):
        app = self.module["Pet"]()
        apply_calls = []
        original_apply = app.apply_settings
        app.apply_settings = lambda settings: (apply_calls.append(dict(settings)), original_apply(settings))[1]
        try:
            opening_scale = app.settings["window_scale_percent"]
            app.show_settings()
            app.update_idletasks()
            widgets = self.descendants(app.settings_dialog)
            scales = [widget for widget in widgets if widget.winfo_class() == "Scale"]
            scale = next(widget for widget in scales if float(widget.cget("to")) == 200.0)
            scale.set(150)
            app.update_idletasks()
            self.assertEqual(app.settings["window_scale_percent"], opening_scale)
            self.assertEqual(apply_calls, [])
            buttons = {
                widget.cget("text"): widget
                for widget in widgets
                if widget.winfo_class() == "Button"
            }
            buttons["应用"].invoke()
            self.assertEqual(app.settings["window_scale_percent"], 150)
            self.assertEqual((app.settings["window_width"], app.settings["window_height"]), (495, 207))
            buttons["恢复默认值"].invoke()
            self.assertEqual(int(scale.get()), 100)
        finally:
            self.destroy_app(app)

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
            self.destroy_app(app)

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
            self.destroy_app(app)

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
            self.destroy_app(app)

    def test_restore_defaults_then_save_explicitly_replaces_protected_configuration(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                app.settings_path.write_text("{damaged", encoding="utf-8")
                app.show_settings()
                app.update_idletasks()
                buttons = {
                    widget.cget("text"): widget
                    for widget in self.descendants(app.settings_dialog)
                    if widget.winfo_class() == "Button"
                }
                buttons["恢复默认值"].invoke()
                buttons["保存"].invoke()
                app.update_idletasks()
                result = app.settings_path.read_text(encoding="utf-8")
                self.assertIn('"schema_version": 1', result)
                self.assertNotEqual(result, "{damaged")
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_rejected_ordinary_save_keeps_dialog_open_and_source_unchanged(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                app.settings_path.write_text("{damaged", encoding="utf-8")
                app.show_settings()
                app.update_idletasks()
                dialog = app.settings_dialog
                buttons = {
                    widget.cget("text"): widget
                    for widget in self.descendants(dialog)
                    if widget.winfo_class() == "Button"
                }
                with mock.patch("ui.settings_dialog.messagebox.showwarning") as warning:
                    buttons["保存"].invoke()
                self.assertTrue(dialog.winfo_exists())
                self.assertEqual(app.settings_path.read_text(encoding="utf-8"), "{damaged")
                warning.assert_called_once()
        finally:
            if app.settings_dialog is not None and app.settings_dialog.winfo_exists():
                app.settings_dialog.destroy()
            self.destroy_app(app)

    def test_pet_renders_five_rows_and_compact_mode_restores_container(self):
        app = self.module["Pet"]()
        try:
            app.latest_activity = {"active": 1, "detail": "工具调用", "progress": "活动对话 1 个"}
            app.render_status()
            self.assertEqual(
                tuple(app.text.labels),
                ("activity", "progress", "primary_5h", "weekly", "reset_credit"),
            )
            self.assertEqual(app.text.row_values()["progress"], "活动对话 1 个")
            app.set_compact(True)
            self.assertEqual(app.text.winfo_manager(), "")
            app.set_compact(False)
            self.assertEqual(app.text.winfo_manager(), "pack")
        finally:
            self.destroy_app(app)

    def test_apply_scale_updates_geometry_fonts_wrap_and_padding_together(self):
        import tkinter.font as tkfont

        app = self.module["Pet"]()
        try:
            app.apply_settings({**app.settings, "window_scale_percent": 150})
            app.update_idletasks()
            self.assertEqual(app.window_metrics.scale_percent, 150)
            self.assertTrue(app.geometry().startswith("495x207"))
            text_font = tkfont.Font(root=app, font=next(iter(app.text.labels.values())).cget("font"))
            self.assertEqual(text_font.cget("size"), 15)
            for label in app.text.labels.values():
                self.assertEqual(int(label.cget("wraplength")), 390)
            self.assertEqual(len(app.battery.cells), 10)
            self.assertEqual(app.battery.winfo_manager(), "pack")
        finally:
            self.destroy_app(app)

    def test_apply_scale_uses_window_dpi_without_persisting_physical_geometry(self):
        app = self.module["Pet"]()
        try:
            with mock.patch.object(
                self.module["_main_window"], "dpi_for_window", return_value=120
            ):
                app.apply_settings(
                    {**app.settings, "window_scale_percent": 150}
                )
            self.assertEqual(
                (app.settings["window_width"], app.settings["window_height"]),
                (495, 207),
            )
            self.assertEqual(
                (app.window_metrics.width, app.window_metrics.height),
                (619, 259),
            )
        finally:
            self.destroy_app(app)

    def test_hide_show_and_compact_expand_preserve_current_scale(self):
        app = self.module["Pet"]()
        app.save_settings = lambda **_kwargs: True
        try:
            app.apply_settings({**app.settings, "window_scale_percent": 150})
            app.hide_window()
            self.assertTrue(app.hidden)
            self.assertEqual(float(app.attributes("-alpha")), 0.0)
            app.show_window()
            app.update_idletasks()
            self.assertFalse(app.hidden)
            self.assertTrue(app.geometry().startswith("495x207"))
            app.set_compact(True)
            app.update_idletasks()
            self.assertFalse(app.geometry().startswith("495x207"))
            app.set_compact(False)
            app.update_idletasks()
            self.assertTrue(app.geometry().startswith("495x207"))
            self.assertEqual(app.window_metrics.scale_percent, 150)
        finally:
            self.destroy_app(app)

    def test_scale_application_keeps_five_row_identities(self):
        app = self.module["Pet"]()
        try:
            identities = {key: str(value) for key, value in app.text.labels.items()}
            app.apply_settings({**app.settings, "window_scale_percent": 80})
            app.apply_settings({**app.settings, "window_scale_percent": 200})
            self.assertEqual({key: str(value) for key, value in app.text.labels.items()}, identities)
            self.assertEqual(len(app.text.labels), 5)
        finally:
            self.destroy_app(app)

    def test_pet_uses_pure_controllers_and_tracks_replaced_settings_path(self):
        app = self.module["Pet"]()
        try:
            self.assertIs(app.refresh_controller, app.application_controller.refresh)
            self.assertIs(app.refresh_scheduler, app.application_controller.quota)
            self.assertIs(app.compact_state, app.presentation_controller.compact)
            with tempfile.TemporaryDirectory() as directory:
                replacement = Path(directory) / "settings.json"
                app.settings_path = replacement
                self.assertEqual(app.settings_controller.path, replacement)
                self.assertTrue(app.save_settings())
                self.assertTrue(replacement.exists())
        finally:
            self.destroy_app(app)


if __name__ == "__main__":
    unittest.main()
