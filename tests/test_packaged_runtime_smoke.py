"""Pure checks supporting the Windows packaged-runtime lifecycle smoke."""

from __future__ import annotations

import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from packaged_runtime_smoke import live_process_tree_ids, pe_subsystem, process_tree_ids


class PackagedRuntimeSmokeTests(unittest.TestCase):
    def test_zip_direct_use_boundary_isolates_user_paths_and_strips_source_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import packaged_runtime_smoke as smoke

            boundary = smoke.zip_direct_use_boundary(root, {"PATH": "C:/Windows", "PYTHONPATH": "C:/source"})

            self.assertEqual(boundary.settings_file, root / "User" / ".codex" / "codex-windows-status-pet.json")
            self.assertEqual(boundary.install_root, root / "Local" / "Programs" / "CodexStatusPet")
            self.assertEqual(
                boundary.shortcut,
                root / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Codex Windows Status Pet.lnk",
            )
            self.assertEqual(boundary.environment["USERPROFILE"], str(root / "User"))
            self.assertEqual(boundary.environment["LOCALAPPDATA"], str(root / "Local"))
            self.assertEqual(boundary.environment["APPDATA"], str(root / "Roaming"))
            self.assertEqual(
                boundary.environment["HOMEDRIVE"] + boundary.environment["HOMEPATH"],
                str(root / "User"),
            )
            self.assertNotIn("PYTHONPATH", boundary.environment)

    def test_zip_direct_use_exit_preserves_settings_without_installed_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            import packaged_runtime_smoke as smoke

            boundary = smoke.zip_direct_use_boundary(root)
            boundary.settings_file.parent.mkdir(parents=True)
            expected_settings = {"schema_version": 1, "x": 30, "y": 120, "language": "zh-CN"}
            boundary.settings_file.write_text('{"schema_version": 1, "x": 30, "y": 120, "language": "zh-CN", "alpha": 0.95}\n', encoding="utf-8")

            smoke.assert_zip_direct_use_exit(boundary, expected_settings)

    def test_zip_direct_use_launch_uses_the_extracted_runtime_and_isolated_environment(self):
        import packaged_runtime_smoke as smoke

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            boundary = smoke.zip_direct_use_boundary(root, {"PATH": "C:/Windows"})
            executable = root / "extract" / "CodexStatusPet" / "CodexStatusPet.exe"
            process = mock.Mock()
            with mock.patch.object(smoke.subprocess, "Popen", return_value=process) as popen:
                self.assertIs(smoke.launch_zip_direct_executable(executable, boundary), process)

            popen.assert_called_once_with(
                [str(executable)],
                cwd=str(executable.parent),
                env=boundary.environment,
            )

    def test_duplicate_notice_is_not_ready_for_only_a_pyinstaller_hidden_window(self):
        import packaged_runtime_smoke as smoke

        with (
            mock.patch.object(smoke, "_window_handles_for_processes", return_value=[101]),
            mock.patch.object(smoke, "_window_class_name", return_value="PyInstallerOnefileHiddenWindow"),
            mock.patch.object(smoke, "_window_is_responsive", return_value=True),
            mock.patch.object(smoke, "_live_process_tree_ids", return_value=frozenset({99})),
        ):
            self.assertFalse(smoke.duplicate_notice_ready(99))

    def test_duplicate_dialog_handles_excludes_pyinstaller_hidden_windows(self):
        import packaged_runtime_smoke as smoke

        with (
            mock.patch.object(smoke, "_window_handles_for_processes", return_value=[101, 102]),
            mock.patch.object(smoke, "_window_class_name", side_effect=["#32770", "PyInstallerOnefileHiddenWindow"]),
            mock.patch.object(smoke, "_live_process_tree_ids", return_value=frozenset({99})),
        ):
            self.assertEqual(smoke._duplicate_dialog_handles(99), [101])

    def test_duplicate_confirmation_uses_the_native_ok_command(self):
        import packaged_runtime_smoke as smoke

        user32 = mock.Mock()
        with (
            mock.patch.object(smoke, "_duplicate_dialog_button_handles", return_value=[202]),
            mock.patch.object(smoke.ctypes, "WinDLL", return_value=user32),
        ):
            smoke._confirm_duplicate_notice(99)

        user32.SendMessageW.assert_called_once_with(202, 0x00F5, 0, 0)

    def test_duplicate_dialog_button_handles_select_only_button_children(self):
        import packaged_runtime_smoke as smoke

        with (
            mock.patch.object(smoke, "_duplicate_dialog_handles", return_value=[101]),
            mock.patch.object(smoke, "_child_window_handles", return_value=[201, 202]),
            mock.patch.object(smoke, "_window_class_name", side_effect=["Static", "Button"]),
        ):
            self.assertEqual(smoke._duplicate_dialog_button_handles(99), [202])

    def test_duplicate_notice_is_ready_only_after_its_window_responds(self):
        import packaged_runtime_smoke as smoke

        with (
            mock.patch.object(smoke, "_duplicate_dialog_handles", return_value=[101]),
            mock.patch.object(smoke, "_window_is_responsive", return_value=True),
        ):
            self.assertTrue(smoke.duplicate_notice_ready(99))

    def test_first_instance_ready_requires_window_and_acquired_mutex(self):
        import packaged_runtime_smoke as smoke

        with (
            mock.patch.object(smoke, "_named_mutex_exists", return_value=True),
            mock.patch.object(smoke, "_window_handles_for_processes", return_value=[101]),
            mock.patch.object(smoke, "_live_process_tree_ids", return_value=frozenset({99})),
        ):
            self.assertTrue(smoke.first_instance_ready(99))

    def test_process_tree_includes_pyinstaller_gui_child_but_not_siblings(self):
        processes = ((100, 1), (101, 100), (102, 101), (200, 1))
        self.assertEqual(process_tree_ids(100, processes), frozenset({100, 101, 102}))
        self.assertEqual(live_process_tree_ids(100, processes), frozenset({100, 101, 102}))
        self.assertEqual(
            live_process_tree_ids(100, ((101, 100), (102, 101), (200, 1))),
            frozenset({101, 102}),
        )

    def test_pe_subsystem_reads_windows_gui_and_rejects_malformed_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "CodexStatusPet.exe"
            payload = bytearray(512)
            payload[:2] = b"MZ"
            struct.pack_into("<I", payload, 0x3C, 0x80)
            payload[0x80:0x84] = b"PE\0\0"
            struct.pack_into("<H", payload, 0x80 + 24 + 68, 2)
            executable.write_bytes(payload)
            self.assertEqual(pe_subsystem(executable), 2)

            executable.write_bytes(b"not a PE")
            with self.assertRaisesRegex(ValueError, "PE"):
                pe_subsystem(executable)


if __name__ == "__main__":
    unittest.main()
