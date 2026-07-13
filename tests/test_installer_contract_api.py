import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.installer_contract_api import installation_paths, verify_checksum
from api.runtime_api import SINGLE_INSTANCE_MUTEX_NAME


class InstallerContractTests(unittest.TestCase):
    def test_checksum_accepts_exact_digest_and_rejects_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "release.zip"
            artifact.write_bytes(b"release")
            digest = hashlib.sha256(b"release").hexdigest()
            self.assertTrue(verify_checksum(artifact, digest))
            with self.assertRaisesRegex(ValueError, "checksum"):
                verify_checksum(artifact, "0" * 64)

    def test_paths_are_per_user_and_purge_targets_only_product_settings(self):
        paths = installation_paths(Path("C:/Users/Tom/AppData/Local"), Path("C:/Users/Tom"))
        self.assertEqual(paths.install_root, Path("C:/Users/Tom/AppData/Local/Programs/CodexStatusPet"))
        self.assertEqual(paths.settings_file, Path("C:/Users/Tom/.codex/codex-windows-status-pet.json"))
        self.assertEqual(paths.settings_file.parent, Path("C:/Users/Tom/.codex"))
        self.assertEqual(paths.settings_file.name, "codex-windows-status-pet.json")

    def test_installer_and_runtime_share_the_product_instance_mutex_name(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertEqual(SINGLE_INSTANCE_MUTEX_NAME, "Local\\CodexWindowsStatusPet")
        self.assertIn(SINGLE_INSTANCE_MUTEX_NAME, installer)
        self.assertIn("OpenExisting", installer)
        self.assertIn("CloseMainWindow", installer)
        self.assertIn("Wait-Process", installer)

    def test_installer_checksum_uses_dotnet_sha256_without_the_optional_get_filehash_cmdlet(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertNotIn("Get-FileHash", installer)
        self.assertIn("[Security.Cryptography.SHA256]::Create()", installer)
        self.assertIn("[IO.File]::OpenRead", installer)

    def test_installer_creates_a_missing_install_parent_before_moving_the_runtime(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        parent_creation = "New-Item -ItemType Directory -Force -Path $installParent"
        runtime_move = "Move-Item -LiteralPath $runtime -Destination $installRoot"
        self.assertIn(parent_creation, installer)
        self.assertLess(installer.index(parent_creation), installer.index(runtime_move))

    def test_installer_requires_manifest_version_to_match_the_resolved_release(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("ExpectedVersion", installer)
        self.assertIn("$manifest.version -ne $ExpectedVersion", installer)


if __name__ == "__main__":
    unittest.main()
