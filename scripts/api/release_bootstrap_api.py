"""Pure selection rules for authenticated GitHub Release deployment."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .release_artifact_api import release_archive_name


class ReleaseResolutionError(ValueError):
    """Raised before acquisition when a Release is not a usable stable source."""


@dataclass(frozen=True)
class ReleaseAssets:
    version: str
    zip_name: str
    checksum_name: str
    installer_name: str


def select_release_assets(release):
    """Return the required assets for one stable semantic GitHub Release."""
    if not isinstance(release, dict) or release.get("isDraft") or release.get("isPrerelease"):
        raise ReleaseResolutionError("release must be a stable published Release")
    tag = release.get("tagName")
    match = re.fullmatch(r"v(\d+\.\d+\.\d+)", str(tag))
    if match is None:
        raise ReleaseResolutionError("release tag must be semantic vMAJOR.MINOR.PATCH")
    version = match.group(1)
    zip_name = release_archive_name(version)
    required = (zip_name, f"{zip_name}.sha256", "install.ps1")
    names = {asset.get("name") for asset in release.get("assets", ()) if isinstance(asset, dict)}
    missing = [name for name in required if name not in names]
    if missing:
        raise ReleaseResolutionError("release required asset is missing: " + ", ".join(missing))
    return ReleaseAssets(
        version=version,
        zip_name=zip_name,
        checksum_name=f"{zip_name}.sha256",
        installer_name="install.ps1",
    )
