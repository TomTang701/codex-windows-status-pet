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


if __name__ == "__main__":
    unittest.main()
