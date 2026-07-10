import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.activity_api import snapshot_activity
from api.config_api import DEFAULT_SETTINGS, load_settings, save_settings_atomic


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


if __name__ == "__main__":
    unittest.main()
