"""Pure installer safety contracts shared by tests and release tooling."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .release_artifact_api import sha256_file


@dataclass(frozen=True)
class InstallationPaths:
    install_root: Path
    settings_file: Path


def installation_paths(local_app_data, user_profile):
    """Return the only permitted per-user product and settings paths."""
    return InstallationPaths(
        install_root=Path(local_app_data) / "Programs" / "CodexStatusPet",
        settings_file=Path(user_profile) / ".codex" / "codex-windows-status-pet.json",
    )


def verify_checksum(artifact, expected):
    """Fail closed unless a supplied SHA-256 matches the exact artifact."""
    actual = sha256_file(artifact)
    if actual.lower() != str(expected).strip().lower():
        raise ValueError("release checksum does not match")
    return True
