import json
import logging
import os
import queue
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.activity_api import snapshot_activity
from api.config_api import DEFAULT_SETTINGS, backup_settings_path, load_settings, restore_settings_backup, save_settings_atomic


def stamp(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat().replace("+00:00", "Z")


class ConfigApiTests(unittest.TestCase):
    def test_invalid_values_fall_back_field_by_field(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"alpha": "bad", "x": "bad", "topmost": "false", "background_color": "not-a-color"}), encoding="utf-8")
            settings, warnings = load_settings(path)
            self.assertEqual(settings["alpha"], DEFAULT_SETTINGS["alpha"])
            self.assertEqual(settings["x"], DEFAULT_SETTINGS["x"])
            self.assertFalse(settings["topmost"])
            self.assertEqual(settings["background_color"], DEFAULT_SETTINGS["background_color"])
            self.assertGreaterEqual(len(warnings), 3)

    def test_atomic_save_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 4151, "y": 1248})
            settings, warnings = load_settings(path)
            self.assertEqual((settings["x"], settings["y"]), (4151, 1248))
            self.assertEqual(warnings, [])
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])

    def test_save_retains_previous_settings_and_restore_uses_valid_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 100})
            save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 200})
            self.assertTrue(backup_settings_path(path).exists())
            self.assertTrue(restore_settings_backup(path))
            settings, warnings = load_settings(path)
            self.assertEqual(settings["x"], 100)
            self.assertEqual(warnings, [])

    def test_malformed_settings_backup_is_not_restored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            backup_settings_path(path).write_text("not-json", encoding="utf-8")
            self.assertFalse(restore_settings_backup(path))

    def test_malformed_current_settings_are_not_promoted_to_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("not-json", encoding="utf-8")
            save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 300})
            self.assertFalse(backup_settings_path(path).exists())

    def test_new_numeric_settings_are_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({
                "window_width": 99999,
                "window_height": 1,
                "refresh_interval_seconds": 99,
                "scale_mode": "proportional",
            }), encoding="utf-8")
            settings, warnings = load_settings(path)
            self.assertEqual(settings["window_width"], 1200)
            self.assertEqual(settings["window_height"], 80)
            self.assertEqual(settings["refresh_interval_seconds"], 10)
            self.assertEqual(settings["scale_mode"], "proportional")

    def test_compact_setting_uses_strict_boolean_normalization(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"compact_when_idle": "true"}), encoding="utf-8")
            settings, _warnings = load_settings(path)
            self.assertTrue(settings["compact_when_idle"])

    def test_utf8_bom_settings_file_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"x": 4151, "y": 1248}), encoding="utf-8-sig")
            settings, warnings = load_settings(path)
            self.assertEqual((settings["x"], settings["y"]), (4151, 1248))
            self.assertEqual(warnings, [])


class ActivityApiTests(unittest.TestCase):
    def write_session(self, directory, records):
        path = Path(directory) / "session.jsonl"
        path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
        os.utime(path, (1000, 1000))
        return path

    def test_recent_event_keeps_long_running_task_active(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(directory, [
                {"timestamp": stamp(100), "type": "event_msg", "payload": {"type": "task_started"}},
                {"timestamp": stamp(950), "type": "response_item", "payload": {"type": "reasoning"}},
            ])
            result = snapshot_activity(Path(directory), stale_seconds=600, now=1000)
            self.assertEqual(result["active"], 1)
            self.assertEqual(result["progress"], "活动对话 1 个")

    def test_old_task_is_not_active(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(directory, [
                {"timestamp": stamp(100), "type": "event_msg", "payload": {"type": "task_started"}},
                {"timestamp": stamp(300), "type": "response_item", "payload": {"type": "reasoning"}},
            ])
            result = snapshot_activity(Path(directory), stale_seconds=600, now=1000)
            self.assertEqual(result["active"], 0)

    def test_malformed_session_line_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.jsonl"
            path.write_text("not-json\n", encoding="utf-8")
            os.utime(path, (1000, 1000))
            result = snapshot_activity(Path(directory), now=1000)
            self.assertEqual(result["active"], 0)

    def test_unchanged_session_uses_parse_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(directory, [
                {"timestamp": stamp(950), "type": "event_msg", "payload": {"type": "task_started"}},
            ])
            cache = {}
            first = snapshot_activity(Path(directory), now=1000, cache=cache)
            cached_value = next(iter(cache.values()))
            second = snapshot_activity(Path(directory), now=1001, cache=cache)
            self.assertEqual(first, second)
            self.assertIs(cached_value, next(iter(cache.values())))


class DiagnosticsAndTrayTests(unittest.TestCase):
    def test_tray_failure_is_reported_to_ui_queue(self):
        module = __import__("codex_status_pet")
        tray = module.TrayIcon3.__new__(module.TrayIcon3)
        tray.actions = queue.Queue()

        class FailedIcon:
            def run(self):
                raise RuntimeError("injected tray failure")

        tray.icon = FailedIcon()
        previous_level = logging.root.manager.disable
        logging.disable(logging.CRITICAL)
        try:
            tray._run()
        finally:
            logging.disable(previous_level)
        self.assertEqual(tray.actions.get_nowait(), "tray_error")


if __name__ == "__main__":
    unittest.main()
