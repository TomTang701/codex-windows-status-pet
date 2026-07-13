"""Pure selection rules for public GitHub Release deployment."""

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
    zip_url: str
    checksum_url: str
    installer_url: str


RELEASES_API = "https://api.github.com/repos/TomTang701/codex-windows-status-pet/releases"


def release_metadata_url(tag=None):
    """Return the public REST endpoint for latest or one exact stable tag."""
    if tag is None:
        return f"{RELEASES_API}/latest"
    if re.fullmatch(r"v\d+\.\d+\.\d+", str(tag)) is None:
        raise ReleaseResolutionError("requested release tag must be vMAJOR.MINOR.PATCH")
    return f"{RELEASES_API}/tags/{tag}"


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
    assets = {
        asset.get("name"): asset
        for asset in release.get("assets", ())
        if isinstance(asset, dict) and asset.get("name")
    }
    missing = [name for name in required if name not in assets]
    if missing:
        raise ReleaseResolutionError("release required asset is missing: " + ", ".join(missing))
    missing_urls = [name for name in required if not assets[name].get("browser_download_url")]
    if missing_urls:
        raise ReleaseResolutionError("release asset download URL is missing: " + ", ".join(missing_urls))
    return ReleaseAssets(
        version=version,
        zip_name=zip_name,
        checksum_name=f"{zip_name}.sha256",
        installer_name="install.ps1",
        zip_url=assets[zip_name]["browser_download_url"],
        checksum_url=assets[f"{zip_name}.sha256"]["browser_download_url"],
        installer_url=assets["install.ps1"]["browser_download_url"],
    )
