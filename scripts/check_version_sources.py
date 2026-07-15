"""Ensure all runtime and release-facing version sources agree."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r'^(?:APP_VERSION|DEFAULT_CLIENT_VERSION)\s*=\s*"([^"]+)"', re.MULTILINE)
CHANGELOG_VERSION = re.compile(r"^##\s+(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\b", re.MULTILINE)


def check(root: Path = ROOT):
    errors = []
    manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    manifest_version = manifest["version"].split("+", 1)[0]
    sources = {
        ".codex-plugin/plugin.json": manifest_version,
    }
    for relative, symbol in (
        ("scripts/ui/main_window.py", "APP_VERSION"),
        ("scripts/api/codex_transport_api.py", "DEFAULT_CLIENT_VERSION"),
    ):
        text = (root / relative).read_text(encoding="utf-8")
        match = re.search(rf"^{symbol}\s*=\s*\"([^\"]+)\"", text, re.MULTILINE)
        if not match:
            errors.append(f"missing {symbol}: {relative}")
        else:
            sources[relative] = match.group(1)
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    match = CHANGELOG_VERSION.search(changelog)
    if not match:
        errors.append("missing semantic version heading in CHANGELOG.md")
    else:
        sources["CHANGELOG.md"] = match.group(1)
    versions = set(sources.values())
    if len(versions) > 1:
        errors.append("version sources differ: " + ", ".join(f"{path}={value}" for path, value in sources.items()))
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("version sources passed")
