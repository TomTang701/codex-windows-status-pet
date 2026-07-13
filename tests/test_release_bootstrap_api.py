import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.release_bootstrap_api import ReleaseResolutionError, select_release_assets


class ReleaseBootstrapTests(unittest.TestCase):
    def test_selects_one_stable_release_zip_checksum_and_installer(self):
        release = {
            "tagName": "v0.9.0",
            "isDraft": False,
            "isPrerelease": False,
            "assets": [
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip"},
                {"name": "CodexStatusPet-v0.9.0-win11-x64.zip.sha256"},
                {"name": "install.ps1"},
            ],
        }

        selection = select_release_assets(release)

        self.assertEqual(selection.version, "0.9.0")
        self.assertEqual(selection.zip_name, "CodexStatusPet-v0.9.0-win11-x64.zip")
        self.assertEqual(selection.checksum_name, "CodexStatusPet-v0.9.0-win11-x64.zip.sha256")
        self.assertEqual(selection.installer_name, "install.ps1")

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

    def test_bootstrap_uses_authenticated_gh_release_assets_and_the_existing_installer(self):
        bootstrap = (Path(__file__).parents[1] / "scripts" / "install_release.ps1").read_text(encoding="utf-8")
        self.assertIn("gh auth status", bootstrap)
        self.assertIn("'release', 'view'", bootstrap)
        self.assertIn("gh release download", bootstrap)
        self.assertIn("install.ps1", bootstrap)
        self.assertIn("$expectedVersion = $Matches[1]", bootstrap)
        self.assertIn("-ExpectedVersion $expectedVersion", bootstrap)
        self.assertNotIn("$releaseArguments.Insert", bootstrap)
        self.assertIn("$releaseArguments = @('release', 'view', $Tag", bootstrap)
        self.assertNotIn("GITHUB_TOKEN", bootstrap)
        self.assertNotIn("gh auth token", bootstrap)


if __name__ == "__main__":
    unittest.main()
