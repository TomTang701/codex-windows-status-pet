import json
import logging
import os
import queue
import sys
import tempfile
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.activity_api import snapshot_activity
from api.config_api import ConfigWriteProtectedError, CONFIG_SCHEMA_VERSION, DEFAULT_SETTINGS, backup_settings_path, load_settings, normalize_settings, restore_settings_backup, save_settings_atomic
from api.status_snapshot_api import build_status_snapshot


def stamp(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat().replace("+00:00", "Z")


class ConfigApiTests(unittest.TestCase):
    def test_battery_source_defaults_to_weekly_and_rejects_invalid_values(self):
        for raw in (
            {},
            {"battery_quota_source": None},
            {"battery_quota_source": "other"},
            {"battery_quota_source": 0},
        ):
            settings, _warnings = normalize_settings(raw)
            self.assertEqual(settings["battery_quota_source"], "weekly")
        settings, _warnings = normalize_settings({"battery_quota_source": "primary_5h"})
        self.assertEqual(settings["battery_quota_source"], "primary_5h")
        _settings, warnings = normalize_settings({"battery_quota_source": "other"})
        self.assertIn("battery_quota_source is invalid; weekly retained", warnings)

    def test_quota_row_visibility_defaults_and_normalizes_independently(self):
        settings, warnings = normalize_settings(
            {
                "show_primary_5h": False,
                "show_weekly": "off",
                "show_reset_credit": 1,
            }
        )
        self.assertFalse(settings["show_primary_5h"])
        self.assertFalse(settings["show_weekly"])
        self.assertTrue(settings["show_reset_credit"])
        self.assertEqual(warnings, [])
        self.assertTrue(DEFAULT_SETTINGS["show_primary_5h"])

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

    def test_malformed_current_settings_are_preserved_and_not_promoted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("not-json", encoding="utf-8")
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 300})
            self.assertEqual(path.read_text(encoding="utf-8"), "not-json")
            self.assertFalse(backup_settings_path(path).exists())

    def test_legacy_numeric_settings_are_bounded_then_canonicalized(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({
                "window_width": 99999,
                "window_height": 1,
                "refresh_interval_seconds": 99,
                "scale_mode": "proportional",
            }), encoding="utf-8")
            settings, warnings = load_settings(path)
            self.assertEqual(settings["window_scale_percent"], 145)
            self.assertEqual(settings["window_width"], 478)
            self.assertEqual(settings["window_height"], 200)
            self.assertEqual(settings["font_size"], 14)
            self.assertEqual(settings["refresh_interval_seconds"], 10)
            self.assertEqual(settings["scale_mode"], "proportional")

    def test_legacy_geometry_migrates_to_canonical_scale_and_derived_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({
                "window_width": 660,
                "window_height": 138,
                "font_size": 19,
                "scale_mode": "free",
                "x": 4151,
            }), encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 140)
            self.assertEqual((result.settings["window_width"], result.settings["window_height"]), (462, 193))
            self.assertEqual(result.settings["font_size"], 14)
            self.assertEqual(result.settings["scale_mode"], "proportional")
            self.assertEqual(result.settings["x"], 4151)
            self.assertTrue(result.writable)

    def test_new_scale_overrides_conflicting_legacy_fields_and_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings_atomic(path, {
                **DEFAULT_SETTINGS,
                "window_scale_percent": 150,
                "window_width": 180,
                "window_height": 800,
                "font_size": 8,
                "scale_mode": "free",
            })
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 150)
            self.assertEqual((result.settings["window_width"], result.settings["window_height"]), (495, 207))
            self.assertEqual(result.settings["font_size"], 15)
            self.assertEqual(result.settings["scale_mode"], "proportional")
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(raw["schema_version"], 1)

    def test_normalized_save_persists_canonical_and_derived_downgrade_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings, warnings = load_settings(Path(directory) / "missing.json")
            self.assertEqual(warnings, [])
            settings["window_scale_percent"] = 150
            normalized, warnings = normalize_settings(settings)
            self.assertEqual(warnings, [])
            save_settings_atomic(path, normalized)
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(raw["window_scale_percent"], 150)
            self.assertEqual((raw["window_width"], raw["window_height"]), (495, 207))
            self.assertEqual(raw["font_size"], 15)
            self.assertEqual(raw["scale_mode"], "proportional")

    def test_invalid_new_scale_is_protected_and_uses_safe_default(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 1, "window_scale_percent": "bad"})
            path.write_text(original, encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings["window_scale_percent"], 100)
            self.assertFalse(result.writable)
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, result.settings)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_future_schema_scale_remains_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "window_scale_percent": 150})
            path.write_text(original, encoding="utf-8")
            result = load_settings(path)
            self.assertEqual(result.settings, DEFAULT_SETTINGS)
            self.assertFalse(result.writable)
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, result.settings)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_legacy_auto_compact_input_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"compact_when_idle": "true"}), encoding="utf-8")
            settings, _warnings = load_settings(path)
            self.assertNotIn("compact_when_idle", settings)
            self.assertFalse(settings["compact"])

    def test_language_and_manual_compact_are_additive_legacy_safe_settings(self):
        missing, _warnings = normalize_settings({})
        self.assertEqual(missing["language"], "en")
        self.assertFalse(missing["compact"])
        selected, _warnings = normalize_settings({"language": "zh-CN", "compact": "true"})
        self.assertEqual(selected["language"], "zh-CN")
        self.assertTrue(selected["compact"])
        legacy, _warnings = normalize_settings({"compact_when_idle": True})
        self.assertFalse(legacy["compact"])
        self.assertNotIn("compact_when_idle", legacy)
        invalid, warnings = normalize_settings({"language": "fr", "compact": "invalid"})
        self.assertEqual(invalid["language"], "en")
        self.assertFalse(invalid["compact"])
        self.assertIn("language is invalid; English retained", warnings)
        self.assertIn("compact is invalid; default retained", warnings)

    def test_utf8_bom_settings_file_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"x": 4151, "y": 1248}), encoding="utf-8-sig")
            settings, warnings = load_settings(path)
            self.assertEqual((settings["x"], settings["y"]), (4151, 1248))
            self.assertEqual(warnings, [])

    def test_legacy_settings_migrate_to_current_schema_in_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"x": 4151}), encoding="utf-8")
            settings, warnings = load_settings(path)
            self.assertEqual(settings["schema_version"], CONFIG_SCHEMA_VERSION)
            self.assertEqual(settings["x"], 4151)
            self.assertEqual(warnings, [])

    def test_unknown_settings_schema_falls_back_safely(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"schema_version": 99, "x": 4151}), encoding="utf-8")
            settings, warnings = load_settings(path)
            self.assertEqual(settings, DEFAULT_SETTINGS)
            self.assertTrue(any("unsupported settings schema" in warning for warning in warnings))
            result = load_settings(path)
            self.assertEqual(result.schema_status, "unsupported")
            self.assertFalse(result.writable)

    def test_future_schema_is_preserved_by_ordinary_save(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = json.dumps({"schema_version": 99, "future": {"value": 1}})
            path.write_text(original, encoding="utf-8")
            with self.assertRaises(ConfigWriteProtectedError):
                save_settings_atomic(path, DEFAULT_SETTINGS)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertFalse(backup_settings_path(path).exists())

    def test_non_object_and_invalid_current_settings_are_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            for raw in ("[]", json.dumps({"schema_version": 1, "alpha": "bad"})):
                with self.subTest(raw=raw):
                    path = Path(directory) / "settings.json"
                    path.write_text(raw, encoding="utf-8")
                    with self.assertRaises(ConfigWriteProtectedError):
                        save_settings_atomic(path, DEFAULT_SETTINGS)
                    self.assertEqual(path.read_text(encoding="utf-8"), raw)

    def test_explicit_reset_may_replace_protected_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("{damaged", encoding="utf-8")
            save_settings_atomic(path, {**DEFAULT_SETTINGS, "x": 4151}, allow_unsafe_overwrite=True)
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(raw["schema_version"], CONFIG_SCHEMA_VERSION)
            self.assertEqual(raw["x"], 4151)
            self.assertFalse(backup_settings_path(path).exists())

    def test_save_always_persists_current_schema_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            save_settings_atomic(path, {"x": 4151})
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(raw["schema_version"], CONFIG_SCHEMA_VERSION)


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
            self.assertEqual(result["activity_state"], "thinking")
            self.assertEqual(result["progress_state"], "active_conversations")

    def test_activity_snapshot_emits_semantic_state_not_localized_text(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(directory, [
                {"timestamp": stamp(100), "type": "event_msg", "payload": {"type": "task_started"}},
                {"timestamp": stamp(950), "type": "response_item", "payload": {"type": "reasoning"}},
            ])
            result = snapshot_activity(Path(directory), stale_seconds=600, now=1000)
            self.assertEqual(result["active"], 1)
            self.assertEqual(result["activity_state"], "thinking")
            self.assertEqual(result["progress_state"], "active_conversations")
            self.assertNotIn("detail", result)
            self.assertNotIn("progress", result)

    def test_same_real_activity_semantics_localize_at_snapshot_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(directory, [
                {"timestamp": stamp(100), "type": "event_msg", "payload": {"type": "task_started"}},
                {"timestamp": stamp(950), "type": "response_item", "payload": {"type": "reasoning"}},
            ])
            activity = snapshot_activity(Path(directory), stale_seconds=600, now=1000)
            english = build_status_snapshot(activity, {"rateLimits": {}}, language="en")
            chinese = build_status_snapshot(activity, {"rateLimits": {}}, language="zh-CN")
            self.assertEqual(english["rows"]["activity"], "Codex Thinking")
            self.assertEqual(english["rows"]["progress"], "Active conversations 1")
            self.assertEqual(chinese["rows"]["activity"], "Codex 思考中")
            self.assertEqual(chinese["rows"]["progress"], "活动对话 1 个")

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

    def test_multiple_active_sessions_are_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index in (1, 2):
                path = root / f"session-{index}.jsonl"
                path.write_text(json.dumps({
                    "timestamp": stamp(950),
                    "type": "event_msg",
                    "payload": {"type": "task_started"},
                }), encoding="utf-8")
                os.utime(path, (1000, 1000))
            result = snapshot_activity(root, now=1000)
            self.assertEqual(result["active"], 2)
            self.assertEqual(result["progress_state"], "active_conversations")

    def test_recently_completed_session_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_session(Path(directory), [
                {"timestamp": stamp(900), "type": "event_msg", "payload": {"type": "task_started"}},
                {"timestamp": stamp(995), "type": "event_msg", "payload": {"type": "task_complete"}},
            ])
            result = snapshot_activity(Path(directory), now=1000)
            self.assertEqual(
                result,
                {
                    "active": 0,
                    "activity_state": "completed",
                    "progress_state": "recent_conversation_completed",
                },
            )

    def test_file_stat_race_does_not_abort_directory_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original_rglob = Path.rglob

            def race_rglob(path, pattern):
                if path == root:
                    class VanishingPath:
                        def stat(self):
                            raise OSError("file vanished during scan")

                        def __str__(self):
                            return "vanishing.jsonl"

                    return iter((VanishingPath(),))
                return original_rglob(path, pattern)

            with mock.patch("api.activity_api.Path.rglob", race_rglob):
                result = snapshot_activity(root, now=1000)
            self.assertEqual(result["active"], 0)


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
