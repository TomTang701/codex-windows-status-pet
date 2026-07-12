"""Release-package smoke uses the shipped onedir ZIP, never a source ZIP."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import package_smoke_test
from api.release_artifact_api import ReleaseManifest


class PackageSmokeTests(unittest.TestCase):
    def test_static_smoke_validates_the_versioned_release_zip(self):
        artifact = package_smoke_test.ROOT / ".build" / "release" / (
            "CodexStatusPet-v0.8.0-win11-x64.zip"
        )
        with mock.patch.object(package_smoke_test, "app_version", return_value="0.8.0"), mock.patch.object(
            package_smoke_test, "validate_release_archive", return_value=ReleaseManifest("0.8.0")
        ) as validate:
            result = package_smoke_test.static_package_smoke()

        self.assertEqual(result, artifact)
        validate.assert_called_once_with(artifact, expected_version="0.8.0")


if __name__ == "__main__":
    unittest.main()
