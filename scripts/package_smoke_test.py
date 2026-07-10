"""Validate the files and metadata required for a distributable package."""

from __future__ import annotations

import json
from pathlib import Path
import re
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    app_source = (ROOT / "scripts" / "codex_status_pet.py").read_text(encoding="utf-8")
    app_version = re.search(r'^APP_VERSION\s*=\s*"([^"]+)"', app_source, re.MULTILINE).group(1)
    manifest_base = manifest["version"].split("+", 1)[0]
    assert manifest_base == app_version, (manifest_base, app_version)
    assert manifest["author"]["name"] == "Zixuan Tang"
    for required in ("start_codex_status_pet.cmd", "requirements.txt", "README.md", "scripts/codex_status_pet.py"):
        assert (ROOT / required).is_file(), required
    archive = ROOT / ".build" / "codex-windows-status-pet-smoke.zip"
    archive.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive, "w") as bundle:
        for path in (ROOT / "scripts").rglob("*.py"):
            bundle.write(path, path.relative_to(ROOT))
        for path in (ROOT / ".codex-plugin").glob("*.json"):
            bundle.write(path, path.relative_to(ROOT))
        for name in ("start_codex_status_pet.cmd", "requirements.txt", "README.md", "README.zh-CN.md"):
            bundle.write(ROOT / name, name)
    assert archive.stat().st_size > 0
    print(f"package smoke test passed: {archive}")


if __name__ == "__main__":
    main()
