"""Own configuration source state and durable persistence decisions."""

from __future__ import annotations

from pathlib import Path

from .config_api import load_settings, restore_settings_backup, save_settings_atomic


class SettingsPersistenceController:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.schema_status = "missing"
        self.writable = True

    def set_path(self, path: Path):
        self.path = Path(path)
        self.schema_status = "missing"
        self.writable = True

    def load(self):
        result = load_settings(self.path)
        self.schema_status = result.schema_status
        self.writable = result.writable
        return result

    def save(self, settings, *, allow_unsafe_overwrite=False) -> bool:
        save_settings_atomic(
            self.path,
            settings,
            allow_unsafe_overwrite=allow_unsafe_overwrite,
        )
        self.schema_status = "current"
        self.writable = True
        return True

    def restore_backup(self) -> bool:
        restored = restore_settings_backup(self.path)
        if restored:
            self.load()
        return restored
