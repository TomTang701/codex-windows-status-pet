"""Transactional settings state for Apply, Save, Close, and defaults."""

from __future__ import annotations

from copy import deepcopy


class SettingsSession:
    def __init__(self, persisted_settings):
        self.persisted_settings = deepcopy(persisted_settings)
        self.runtime_settings = deepcopy(persisted_settings)
        self.draft_settings = deepcopy(persisted_settings)
        self.opening_snapshot = deepcopy(persisted_settings)

    def apply(self):
        self.runtime_settings = deepcopy(self.draft_settings)
        return deepcopy(self.runtime_settings)

    def save(self):
        self.apply()
        self.persisted_settings = deepcopy(self.runtime_settings)
        self.opening_snapshot = deepcopy(self.runtime_settings)
        return deepcopy(self.persisted_settings)

    def close(self):
        self.runtime_settings = deepcopy(self.opening_snapshot)
        self.draft_settings = deepcopy(self.opening_snapshot)
        return deepcopy(self.runtime_settings)

    def restore_defaults(self, defaults):
        self.draft_settings = deepcopy(defaults)
        return deepcopy(self.draft_settings)
