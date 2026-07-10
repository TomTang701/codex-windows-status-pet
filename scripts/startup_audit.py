"""Read-only audit for stale Codex Status Pet startup entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LEGACY_NAMES = {"codex status pet.lnk", "codex windows status pet.lnk"}


def audit_startup(startup_folder=None):
    folder = Path(startup_folder) if startup_folder else Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    entries = sorted(path.name for path in folder.iterdir()) if folder.is_dir() else []
    legacy_entries = [name for name in entries if name.lower() in LEGACY_NAMES]
    return {
        "startup_folder": str(folder),
        "entries": entries,
        "legacy_entries": legacy_entries,
        "clean": not legacy_entries,
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
