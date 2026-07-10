"""Read-only audit for stale Codex Status Pet startup entries."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


LEGACY_NAMES = {"codex status pet.lnk", "codex windows status pet.lnk"}
LEGACY_TOKENS = {"codex status pet", "codex windows status pet"}
LEGACY_PATH_MARKER = ".agents\\plugins\\plugins\\codex-windows-status-pet"


def is_legacy_value(name, value):
    text = f"{name} {value}".lower()
    return any(token in text for token in LEGACY_TOKENS) or LEGACY_PATH_MARKER.lower() in text


def read_run_entries():
    if os.name != "nt":
        return []
    try:
        import winreg
    except ImportError:
        return []
    entries = []
    for hive, hive_name in ((winreg.HKEY_CURRENT_USER, "HKCU"), (winreg.HKEY_LOCAL_MACHINE, "HKLM")):
        for key_name in ("Run", "RunOnce"):
            try:
                with winreg.OpenKey(hive, rf"Software\Microsoft\Windows\CurrentVersion\{key_name}") as key:
                    for index in range(winreg.QueryInfoKey(key)[1]):
                        name, value, _kind = winreg.EnumValue(key, index)
                        if is_legacy_value(name, value):
                            entries.append({"hive": hive_name, "key": key_name, "name": name, "value": str(value)})
            except OSError:
                continue
    return entries


def audit_startup(startup_folder=None):
    folder = Path(startup_folder) if startup_folder else Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    entries = sorted(path.name for path in folder.iterdir()) if folder.is_dir() else []
    legacy_entries = [name for name in entries if name.lower() in LEGACY_NAMES]
    run_entries = read_run_entries()
    return {
        "startup_folder": str(folder),
        "entries": entries,
        "legacy_entries": legacy_entries,
        "legacy_run_entries": run_entries,
        "clean": not legacy_entries and not run_entries,
        "action": "report-only; no startup entry was modified",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return failure when a known legacy entry exists")
    args = parser.parse_args()
    result = audit_startup()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.strict and not result["clean"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
