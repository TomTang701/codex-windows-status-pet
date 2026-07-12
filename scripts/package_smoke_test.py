"""Validate the actual versioned Windows release ZIP after it is built."""

from __future__ import annotations

import re
from pathlib import Path

from api.release_artifact_api import release_archive_name, validate_release_archive


ROOT = Path(__file__).resolve().parents[1]


def app_version():
    source = (ROOT / "scripts" / "ui" / "main_window.py").read_text(encoding="utf-8")
    match = re.search(r'^APP_VERSION\s*=\s*"([^"]+)"', source, re.MULTILINE)
    if match is None:
        raise RuntimeError("application version is unavailable")
    return match.group(1)


def static_package_smoke():
    """Validate the exact ZIP that users would download and install."""
    version = app_version()
    artifact = ROOT / ".build" / "release" / release_archive_name(version)
    validate_release_archive(artifact, expected_version=version)
    return artifact


def main():
    artifact = static_package_smoke()
    print(f"package static smoke passed: {artifact}")


if __name__ == "__main__":
    main()
