"""Release-only installed-product lifecycle smoke contracts."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from installed_lifecycle_smoke import (
    ensure_clean_install_root,
    installed_lifecycle_paths,
    installed_process_probe_command,
    main,
    windows_powershell_executable,
)


class InstalledLifecycleSmokeTests(unittest.TestCase):
    def test_source_repairs_stop_the_launched_process_before_settings_assertions(self):
        script = (Path(__file__).parents[1] / "scripts" / "installed_lifecycle_smoke.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(script.count("_stop_installed_processes(paths.install_root)"), 4)

    def test_windows_powershell_executable_uses_the_system_powershell_51_path(self):
        self.assertEqual(
            windows_powershell_executable(Path("C:/Windows")),
            Path("C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"),
        )

    def test_main_writes_success_result_file_after_the_lifecycle_smoke_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            result_file = Path(directory) / "lifecycle-result.json"
            artifact = Path(directory) / "CodexStatusPet-v0.8.0-win11-x64.zip"
            with mock.patch("installed_lifecycle_smoke.installed_lifecycle_smoke", return_value=artifact):
                exit_code = main(["--result-file", str(result_file)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(
                json.loads(result_file.read_text(encoding="utf-8")),
                {"artifact": str(artifact), "passed": True},
            )

    def test_main_passes_an_explicit_previous_release_to_the_upgrade_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_file = root / "lifecycle-result.json"
            previous = root / "CodexStatusPet-v0.8.0-win11-x64.zip"
            artifact = root / "CodexStatusPet-v0.9.0-win11-x64.zip"
            with mock.patch("installed_lifecycle_smoke.installed_lifecycle_smoke", return_value=artifact) as smoke:
                exit_code = main([
                    "--previous-artifact", str(previous),
                    "--result-file", str(result_file),
                ])

            self.assertEqual(exit_code, 0)
            smoke.assert_called_once_with(previous_artifact=previous)

    def test_process_probe_embeds_the_exact_installed_executable_path(self):
        command = installed_process_probe_command(Path("C:/Users/Tom/AppData/Local/Programs/CodexStatusPet/CodexStatusPet.exe"))
        self.assertIn("'C:/Users/Tom/AppData/Local/Programs/CodexStatusPet/CodexStatusPet.exe'", command)
        self.assertNotIn("$args[0]", command)

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
