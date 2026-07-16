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

    def test_installer_discovers_python_and_installs_private_dependencies(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("Find-CompatiblePython", installer)
        self.assertIn("codex-primary-runtime", installer)
        self.assertIn("py.exe", installer)
        self.assertIn("python.exe", installer)
        self.assertIn("runtime-packages", installer)
        self.assertIn("Pillow==12.2.0", (Path(__file__).parents[1] / "requirements-runtime.txt").read_text(encoding="utf-8"))
        self.assertIn("pystray==0.19.5", (Path(__file__).parents[1] / "requirements-runtime.txt").read_text(encoding="utf-8"))

    def test_standalone_installation_skips_python_discovery_and_private_pip(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("$standalone = $manifest.schema_version -eq 1", installer)
        self.assertIn("standalone runtime material is missing", installer)
        standalone = installer.index("$standalone =")
        source_runtime = installer.index("if ($source) {")
        python_discovery = installer.index("$python = Find-CompatiblePython")
        self.assertLess(standalone, source_runtime)
        self.assertLess(source_runtime, python_discovery)
        self.assertIn("-Legacy:$standalone", installer)
        self.assertIn("if ($standalone) {", installer)

    def test_source_python_discovery_enumerates_candidates_and_reports_rejections(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("py.exe", installer)
        self.assertIn("-0p", installer)
        self.assertIn("Checked Python candidates:", installer)
        self.assertIn("Rejected", installer)

    def test_installer_keeps_existing_single_instance_contract_available_to_runtime(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertEqual(SINGLE_INSTANCE_MUTEX_NAME, "Local\\CodexWindowsStatusPet")
        self.assertIn("Start-Process", installer)

    def test_installer_checksum_uses_dotnet_sha256_without_the_optional_get_filehash_cmdlet(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertNotIn("Get-FileHash", installer)
        self.assertIn("[Security.Cryptography.SHA256]::Create()", installer)
        self.assertIn("[IO.File]::OpenRead", installer)

    def test_installer_creates_a_missing_install_parent_before_moving_the_runtime(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        parent_creation = "New-Item -ItemType Directory -Force -Path (Split-Path -Parent $installRoot)"
        runtime_move = "Move-Item -LiteralPath $runtime -Destination $installRoot"
        self.assertIn(parent_creation, installer)
        self.assertLess(installer.index(parent_creation), installer.index(runtime_move))

    def test_installer_requires_manifest_version_to_match_the_resolved_release(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("ExpectedVersion", installer)
        self.assertIn("$manifest.version -eq $ExpectedVersion", installer)
        self.assertIn("$manifest.schema_version -eq 2", installer)
        self.assertIn("scripts/codex_status_pet.py", installer)

    def test_installer_accepts_a_mutually_exclusive_extracted_source_root(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("[string]$SourceRoot", installer)
        self.assertIn("Specify either extracted SourceRoot or the verified artifact parameters, not both.", installer)
        self.assertIn("SourceRoot requires a directory containing release-manifest.json.", installer)

    def test_extracted_source_install_derives_exact_version_and_stages_without_generated_runtime(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("$ExpectedVersion = [string]$sourceManifest.version", installer)
        self.assertIn("Copy-ReleaseSource", installer)
        self.assertIn("@('runtime.json', 'runtime-packages')", installer)
        self.assertIn("SourceRoot cannot be the installed product directory or one of its descendants.", installer)

    def test_installer_snapshots_existing_settings_before_stopping_the_installed_runtime(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        snapshot = "$settingsSnapshot = Join-Path $staging 'settings-before-install.json'"
        stop = "Stop-InstalledProduct"
        restore = "Copy-Item -LiteralPath $settingsSnapshot -Destination $settingsPath -Force"
        self.assertIn("CodexStatusPet.exe", installer)
        self.assertIn("$env:USERPROFILE", installer)
        self.assertIn("Move-Item -LiteralPath $installRoot -Destination $backup", installer)

    def test_installer_has_an_explicit_test_only_failure_after_backup_creation(self):
        installer = (Path(__file__).parents[1] / "install.ps1").read_text(encoding="utf-8")
        switch = "[switch]$TestFailAfterBackup"
        move = "Move-Item -LiteralPath $runtime -Destination $installRoot"
        failure = "if ($TestFailAfterBackup) { throw 'Test failure after backup creation.' }"
        self.assertIn(switch, installer)
        self.assertIn(failure, installer)
        self.assertLess(installer.index(move), installer.index(failure))

    def test_installer_creates_and_uninstaller_removes_both_special_folder_shortcuts(self):
        root = Path(__file__).parents[1]
        installer = (root / "install.ps1").read_text(encoding="utf-8")
        uninstaller = (root / "uninstall.ps1").read_text(encoding="utf-8")
        self.assertIn("[Environment]::GetFolderPath('Desktop')", installer)
        self.assertIn("Microsoft\\Windows\\Start Menu\\Programs", installer)
        self.assertIn("IconLocation", installer)
        self.assertIn("launch.vbs", installer)
        self.assertIn("launch.cmd", installer)
        self.assertIn("[Environment]::GetFolderPath('Desktop')", uninstaller)
        self.assertIn("runtime-packages", (root / "launch.ps1").read_text(encoding="utf-8"))

    def test_installer_and_uninstaller_stop_source_python_by_command_line(self):
        root = Path(__file__).parents[1]
        installer = (root / "install.ps1").read_text(encoding="utf-8")
        uninstaller = (root / "uninstall.ps1").read_text(encoding="utf-8")
        for script in (installer, uninstaller):
            self.assertIn("$_.CommandLine", script)
            self.assertIn("IndexOf", script)
            self.assertIn("[StringComparison]::OrdinalIgnoreCase", script)
        self.assertIn("Wait-Process", uninstaller)
        self.assertIn("for ($attempt = 0; $attempt -lt 20", uninstaller)
        self.assertIn("Installed product directory could not be removed.", uninstaller)

    def test_launcher_resolves_its_root_from_psscriptroot_when_started_by_shortcut(self):
        launcher = (Path(__file__).parents[1] / "launch.ps1").read_text(encoding="utf-8")
        self.assertIn("param([string]$InstallRoot)", launcher)
        self.assertIn("$PSScriptRoot", launcher)
        self.assertNotIn("$MyInvocation.MyCommand.Path", launcher)

    def test_release_contains_a_direct_cmd_fallback_launcher(self):
        root = Path(__file__).parents[1]
        launcher = (root / "launch.cmd").read_text(encoding="utf-8")
        self.assertIn("launch.ps1", launcher)
        self.assertIn("%~dp0", launcher)

    def test_cmd_launcher_installs_unconfigured_extracted_zip_and_starts_configured_copy(self):
        launcher = (Path(__file__).parents[1] / "launch.cmd").read_text(encoding="utf-8")
        self.assertIn('if exist "%ROOT%runtime.json"', launcher)
        self.assertIn('-File "%ROOT%install.ps1" -SourceRoot "%ROOT%."', launcher)
        self.assertIn('-File "%ROOT%launch.ps1"', launcher)

    def test_cmd_launcher_preserves_failure_code_and_supports_noninteractive_use(self):
        launcher = (Path(__file__).parents[1] / "launch.cmd").read_text(encoding="utf-8")
        self.assertIn('set "RESULT=%ERRORLEVEL%"', launcher)
        self.assertIn('CODEX_STATUS_PET_NO_PAUSE', launcher)
        self.assertIn('exit /b %RESULT%', launcher)


if __name__ == "__main__":
    unittest.main()
