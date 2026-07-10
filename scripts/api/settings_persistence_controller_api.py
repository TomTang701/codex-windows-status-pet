"""Own configuration schema state and all durable persistence decisions."""

from __future__ import annotations

from pathlib import Path

from .config_api import load_settings, restore_settings_backup, save_settings_atomic


class SettingsPersistenceController:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.schema_status = "missing"
        self.writable = True

    def load(self):
        result = load_settings(self.path)
        self.schema_status = result.schema_status
        self.writable = result.writable
        return result

    def save(self, settings) -> bool:
        if not self.writable:
            return False
        save_settings_atomic(self.path, settings)
        return True

    def restore_backup(self) -> bool:
        return restore_settings_backup(self.path)

    def authorize_reset(self):
        self.schema_status = "current"
        self.writable = True
