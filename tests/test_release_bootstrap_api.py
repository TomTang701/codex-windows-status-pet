import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import api.release_bootstrap_api as release_bootstrap_api

from api.release_bootstrap_api import ReleaseResolutionError, select_release_assets


class ReleaseBootstrapTests(unittest.TestCase):
    def test_selects_one_stable_release_zip_checksum_and_installer(self):
        release = {
            "tagName": "v0.9.0",
            "isDraft": False,
            "isPrerelease": False,
            "assets": [
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip", "browser_download_url": "https://example.test/product.zip"},
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip.sha256", "browser_download_url": "https://example.test/product.sha256"},
                {"name": "install.ps1", "browser_download_url": "https://example.test/install.ps1"},
            ],
        }

        selection = select_release_assets(release)

        self.assertEqual(selection.version, "0.9.0")
        self.assertEqual(selection.zip_name, "CodexStatusPet-v0.9.0-win11-x64.zip")
        self.assertEqual(selection.checksum_name, "CodexStatusPet-v0.9.0-win11-x64.zip.sha256")
        self.assertEqual(selection.installer_name, "install.ps1")
        self.assertEqual(getattr(selection, "zip_url", None), "https://example.test/product.zip")
        self.assertEqual(getattr(selection, "checksum_url", None), "https://example.test/product.sha256")
        self.assertEqual(getattr(selection, "installer_url", None), "https://example.test/install.ps1")

    def test_default_and_pinned_release_metadata_use_public_rest_endpoints(self):
        self.assertEqual(
            getattr(release_bootstrap_api, "release_metadata_url", lambda *_: None)(),
            "https://api.github.com/repos/TomTang701/codex-windows-status-pet/releases/latest",
        )
        self.assertEqual(
            getattr(release_bootstrap_api, "release_metadata_url", lambda *_: None)("v0.9.0"),
            "https://api.github.com/repos/TomTang701/codex-windows-status-pet/releases/tags/v0.9.0",
        )
        with self.assertRaisesRegex(ReleaseResolutionError, "vMAJOR"):
            release_bootstrap_api.release_metadata_url("latest")

    def test_source_archive_never_substitutes_for_product_asset(self):
        release = {
            "tagName": "v0.9.0",
            "isDraft": False,
            "isPrerelease": False,
            "assets": [
                {"name": "Source code (zip)", "browser_download_url": "https://example.test/source.zip"},
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip.sha256", "browser_download_url": "https://example.test/product.sha256"},
                {"name": "install.ps1", "browser_download_url": "https://example.test/install.ps1"},
            ],
        }
        with self.assertRaisesRegex(ReleaseResolutionError, "required asset"):
            select_release_assets(release)

    def test_missing_asset_download_url_fails_before_installation(self):
        release = {
            "tagName": "v0.9.0",
            "isDraft": False,
            "isPrerelease": False,
            "assets": [
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip"},
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip.sha256", "browser_download_url": "https://example.test/product.sha256"},
                {"name": "install.ps1", "browser_download_url": "https://example.test/install.ps1"},
            ],
        }
        with self.assertRaisesRegex(ReleaseResolutionError, "download URL"):
            select_release_assets(release)

    def test_rejects_draft_prerelease_and_missing_required_assets_before_installation(self):
        incomplete = {
            "tagName": "v0.9.0",
            "isDraft": False,
            "isPrerelease": False,
            "assets": [{"name": "CodexStatusPet-v0.9.0-win11-x64.zip"}],
        }
        with self.assertRaisesRegex(ReleaseResolutionError, "required asset"):
            select_release_assets(incomplete)

        for key in ("isDraft", "isPrerelease"):
            release = dict(incomplete, **{key: True})
            with self.assertRaisesRegex(ReleaseResolutionError, "stable"):
                select_release_assets(release)

    def test_bootstrap_uses_public_rest_release_assets_and_the_existing_installer(self):
        bootstrap = (Path(__file__).parents[1] / "scripts" / "install_release.ps1").read_text(encoding="utf-8")
        self.assertIn("Invoke-RestMethod", bootstrap)
        self.assertIn("$releasesApi/latest", bootstrap)
        self.assertIn("$releasesApi/tags/$Tag", bootstrap)
        self.assertNotIn("gh auth status", bootstrap)
        self.assertNotIn("gh release view", bootstrap)
        self.assertNotIn("gh release download", bootstrap)
        self.assertIn("install.ps1", bootstrap)
        self.assertIn("$expectedVersion = $Matches[1]", bootstrap)
        self.assertIn("-ExpectedVersion ([string]$expectedVersion)", bootstrap)
        self.assertIn("if (-not $?)", bootstrap)
        self.assertNotIn("$LASTEXITCODE -ne 0", bootstrap)

    def test_release_candidate_smoke_uses_the_published_latest_release(self):
        smoke = (Path(__file__).parents[1] / "scripts" / "release_bootstrap_smoke.py").read_text(encoding="utf-8")
        self.assertNotIn('"-Tag", "v1.0.2"', smoke)
        self.assertIn('installed_version =', smoke)
        self.assertIn('f"CodexStatusPet-v{installed_version}-win11-x64.zip"', smoke)
        self.assertNotIn("GITHUB_TOKEN", bootstrap)
        self.assertNotIn("gh auth token", bootstrap)


if __name__ == "__main__":
    unittest.main()
