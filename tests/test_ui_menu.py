import runpy
import sys
import tempfile
import unittest
import gc
import logging
import json
import time
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.display_api import work_area_for_point


class DummyServer:
    def __init__(self, _queue):
        self.proc = None

    def stop(self):
        pass


class DummyTray:
    def __init__(self, _actions):
        self.menu_states = []

    def set_menu_state(self, language, **state):
        self.menu_states.append((language, state))

    def stop(self):
        pass


class MenuInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "codex_status_pet.py"))
        cls.module["AppServer"] = DummyServer
        cls.module["TrayIcon3"] = DummyTray

    def setUp(self):
        self._home = tempfile.TemporaryDirectory()
        self._original_home = Path.home
        Path.home = classmethod(lambda cls: Path(self._home.name))

    def tearDown(self):
        Path.home = self._original_home
        self._home.cleanup()

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
            self.assertEqual(labels, ["Settings", "Always on top  ✓", "Lock position  ○", "Compact  ○", "Hide window", "Exit"])
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

    def test_context_menu_uses_current_runtime_language_without_changing_actions(self):
        app = self.module["Pet"]()
        try:
            app.settings["language"] = "en"
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            labels = [item.cget("text") for item in self.menu_items(app.context_menu)]
            self.assertEqual(labels, ["Settings", "Always on top  ✓", "Lock position  ○", "Compact  ○", "Hide window", "Exit"])
        finally:
            self.destroy_app(app)

    def test_manual_compact_toggle_updates_visual_state_and_persists(self):
        app = self.module["Pet"]()
        try:
            with tempfile.TemporaryDirectory() as directory:
                app.settings_path = Path(directory) / "settings.json"
                self.assertTrue(app.set_manual_compact(True))
                self.assertTrue(app.compact)
                self.assertTrue(app.settings["compact"])
                self.assertTrue(app.load_settings()["compact"])
                self.assertTrue(app.set_manual_compact(False))
                self.assertFalse(app.compact)
                self.assertFalse(app.load_settings()["compact"])
        finally:
            self.destroy_app(app)

    def test_overlay_context_menu_consumes_shared_menu_model(self):
        app = self.module["Pet"]()
        try:
            with mock.patch("ui.context_menu.build_menu_items", wraps=__import__("api.menu_model_api", fromlist=["build_menu_items"]).build_menu_items) as model:
                app.menu(SimpleNamespace(x_root=4200, y_root=200))
            model.assert_called_once_with(
                "en", visible=True,
                topmost=app.settings["topmost"], locked=app.settings["locked"],
                compact=app.settings["compact"],
            )
        finally:
            self.destroy_app(app)

    def test_context_menu_refreshes_shell_identity_for_popup_and_owner(self):
        app = self.module["Pet"]()
        try:
            with mock.patch("ui.context_menu.ensure_overlay_toolwindow") as normalize:
                app.menu(SimpleNamespace(x_root=4200, y_root=200))
                normalize.assert_any_call(app.context_menu.winfo_id())
                app.context_menu.event_generate("<Escape>")
                app.update_idletasks()
                normalize.assert_any_call(app.winfo_id())
        finally:
            self.destroy_app(app)

    def test_context_menu_reasserts_owner_shell_after_focus_transition(self):
        app = self.module["Pet"]()
        try:
            with mock.patch("ui.context_menu.ensure_overlay_toolwindow") as normalize:
                app.menu(SimpleNamespace(x_root=4200, y_root=200))
                app.update()
                time.sleep(0.25)
                app.update()
                owner_calls = [call for call in normalize.call_args_list if call.args == (app.winfo_id(),)]
                self.assertGreaterEqual(len(owner_calls), 2)
        finally:
            self.destroy_app(app)

    def test_main_window_pushes_live_menu_state_to_tray(self):
        app = self.module["Pet"]()
        calls = []
        app.tray.set_menu_state = lambda language, **state: calls.append((language, state))
        app.save_settings = lambda **_kwargs: True
        try:
            app.apply_settings({**app.settings, "topmost": False, "locked": True})
            app.set_manual_compact(True)
            app.hide_window()
            self.assertEqual(
                calls[-1],
                ("en", {"visible": False, "topmost": False, "locked": True, "compact": True}),
            )
            app.show_window()
            self.assertEqual(calls[-1][1]["visible"], True)
        finally:
            self.destroy_app(app)

    def test_new_tray_receives_initial_live_menu_state(self):
        settings_path = Path(self._home.name) / ".codex" / "codex-windows-status-pet.json"
        settings_path.parent.mkdir(parents=True)
        settings_path.write_text(json.dumps({"topmost": False, "compact": True}), encoding="utf-8")
        app = self.module["Pet"]()
        try:
            self.assertEqual(
                app.tray._menu_state,
                {"visible": True, "topmost": False, "locked": False, "compact": True},
            )
        finally:
            self.destroy_app(app)

    def test_compact_menu_checkbox_toggles_without_menu_open_expansion(self):
        app = self.module["Pet"]()
        try:
            app.settings_path = Path(tempfile.gettempdir()) / "codex-status-pet-menu-test.json"
            app.set_manual_compact(True)
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            self.assertTrue(app.compact)
            compact = next(item for item in self.menu_items(app.context_menu) if "Compact" in item.cget("text"))
            self.assertTrue(bool(app.compact_var.get()))
            compact.invoke()
            app.update_idletasks()
            self.assertFalse(app.compact)
            self.assertFalse(app.settings["compact"])
        finally:
            self.destroy_app(app)

    def test_manual_compact_survives_render_hide_show_and_settings_preview(self):
        app = self.module["Pet"]()
        app.save_settings = lambda **_kwargs: True
        try:
            app.set_manual_compact(True)
            app.render_status()
            app.hide_window()
            app.show_window()
            self.assertTrue(app.compact)
            app.show_settings()
            dialog = app.settings_dialog
            language = next(widget for widget in self.descendants(dialog) if widget.winfo_class() == "TCombobox")
            language.set("Simplified Chinese")
            next(widget for widget in self.descendants(dialog) if widget.winfo_class() == "Button" and widget.cget("text") == "Apply").invoke()
            self.assertTrue(app.compact)
            next(widget for widget in self.descendants(dialog) if widget.winfo_class() == "Button" and widget.cget("text") == "关闭").invoke()
            self.assertTrue(app.compact)
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
            self.assertEqual(app.text.row_values()["weekly"], "Weekly 55%")
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
            self.assertEqual(values["progress"], "Quota unavailable")
            self.assertNotIn("transport exploded", "\n".join(values.values()))
            self.assertEqual(app.quota_state.state, "unavailable")
        finally:
            self.destroy_app(app)

    def test_settings_button_is_invokable_once_from_popup(self):
        app = self.module["Pet"]()
        try:
            app.menu(SimpleNamespace(x_root=4200, y_root=200))
            popup = app.context_menu
            settings = next(item for item in self.menu_items(popup) if item.cget("text") == "Settings")
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
            self.assertIn("Opacity", texts)
            self.assertIn("Window size", texts)
            self.assertIn("Battery display content", texts)
            self.assertIn("5-hour", texts)
            self.assertIn("Weekly", texts)
            for removed in ("字体大小", "窗口大小 (宽, 高)", "−", "+", "等比例缩放"):
                self.assertNotIn(removed, texts)
            self.assertIn("Default position (X, Y)", texts)
            self.assertIn("Refresh interval (seconds)", texts)
            for retained in (
                "Always on top", "Lock position", "Font color...", "Background color...",
                "Save", "Apply", "Restore Defaults", "Close",
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
            buttons["Apply"].invoke()
            self.assertEqual(app.settings["window_scale_percent"], 150)
            self.assertEqual((app.settings["window_width"], app.settings["window_height"]), (495, 207))
            buttons["Restore Defaults"].invoke()
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
            hide = next(item for item in self.menu_items(popup) if item.cget("text") == "Hide window")
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
                buttons["Restore Defaults"].invoke()
                buttons["Save"].invoke()
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
                    buttons["Save"].invoke()
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
            self.assertEqual(app.battery.winfo_manager(), "")
            self.assertFalse(app.battery.winfo_ismapped())
            self.assertFalse(app.signal_card.winfo_ismapped())
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

    def test_settings_reapplication_preserves_compact_root_geometry(self):
        app = self.module["Pet"]()
        try:
            app.set_compact(True)
            app.update_idletasks()
            settings_updates = (
                {"locked": not app.settings["locked"]},
                {"topmost": not app.settings["topmost"]},
                {"language": "zh-CN"},
                {"alpha": 0.5},
                {"window_scale_percent": 150},
                {"show_weekly": not app.settings["show_weekly"]},
                {"battery_quota_source": "primary_5h"},
            )
            for update in settings_updates:
                with self.subTest(update=update):
                    app.apply_settings({**app.settings, **update})
                    app.update_idletasks()
                    size = app.winfo_width(), app.winfo_height()
                    self.assertTrue(app.compact)
                    self.assertEqual(size[0], size[1])
        finally:
            self.destroy_app(app)

    def test_compact_drag_uses_compact_bounds_and_persists_canonical_position(self):
        app = self.module["Pet"]()
        app.save_settings = lambda **_kwargs: True
        try:
            with mock.patch.object(
                self.module["_main_window"], "work_area_for_point", return_value=(0, 0, 1920, 1030)
            ):
                app.set_compact(True)
                app.update_idletasks()
                size = app.winfo_width()
                expanded_width = app.window_metrics.width
                for name, target_x, target_y in (
                    ("right", 1920 - size, 120),
                    ("bottom", 120, 1030 - size),
                    ("bottom_right", 1920 - size, 1030 - size),
                ):
                    with self.subTest(anchor=name):
                        safe_calls = []

                        def safe_position(x, y, width=None, height=None):
                            safe_calls.append((x, y, width, height))
                            return x, y

                        app.safe_position = safe_position
                        app.start_drag(
                            SimpleNamespace(x_root=app.winfo_rootx() + 10, y_root=app.winfo_rooty() + 10)
                        )
                        app.drag(SimpleNamespace(x_root=target_x + 10, y_root=target_y + 10))
                        app.update_idletasks()
                        self.assertTrue(app.compact)
                        self.assertEqual((app.winfo_rootx(), app.winfo_rooty()), (target_x, target_y))
                        self.assertEqual(
                            (app.settings["x"], app.settings["y"]),
                            (
                                target_x - (expanded_width - size) if name in ("right", "bottom_right") else target_x,
                                target_y - (app.window_metrics.height - size) if name in ("bottom", "bottom_right") else target_y,
                            ),
                        )
                        self.assertIn((target_x, target_y, size, size), safe_calls)
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
            self.assertIs(app.compact_state, app.compact)
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
