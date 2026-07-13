"""Release-only installed-product lifecycle smoke contracts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from installed_lifecycle_smoke import ensure_clean_install_root, installed_lifecycle_paths


class InstalledLifecycleSmokeTests(unittest.TestCase):
    def test_paths_are_limited_to_the_product_root_shortcut_and_settings_file(self):
        paths = installed_lifecycle_paths(
            local_app_data=Path("C:/Users/Tom/AppData/Local"),
            app_data=Path("C:/Users/Tom/AppData/Roaming"),
            user_profile=Path("C:/Users/Tom"),
        )
        self.assertEqual(
            paths.install_root,
            Path("C:/Users/Tom/AppData/Local/Programs/CodexStatusPet"),
        )
        self.assertEqual(
            paths.shortcut,
            Path("C:/Users/Tom/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Codex Windows Status Pet.lnk"),
        )
        self.assertEqual(
            paths.settings_file,
            Path("C:/Users/Tom/.codex/codex-windows-status-pet.json"),
        )
        self.assertEqual(paths.settings_file.parent, Path("C:/Users/Tom/.codex"))

    def test_existing_product_installation_is_refused_before_lifecycle_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = installed_lifecycle_paths(
                local_app_data=root / "local",
                app_data=root / "roaming",
                user_profile=root / "user",
            )
            paths.install_root.mkdir(parents=True)
            with self.assertRaisesRegex(RuntimeError, "existing installed product"):
                ensure_clean_install_root(paths)


if __name__ == "__main__":
    unittest.main()
