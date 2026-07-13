"""Regression coverage for a packaged launch blocked by an existing instance."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from ui import main_window


class SingleInstanceStartupTests(unittest.TestCase):
    def test_run_explains_when_an_existing_instance_blocks_startup(self):
        with (
            mock.patch.object(main_window.sys, "platform", "win32"),
            mock.patch.object(main_window, "configure_logging"),
            mock.patch.object(main_window, "enable_dpi_awareness"),
            mock.patch.object(main_window, "ensure_single_instance", return_value=False),
            mock.patch.object(main_window, "notify_existing_instance") as notify,
        ):
            with self.assertRaises(SystemExit) as stopped:
                main_window.run()

        self.assertEqual(stopped.exception.code, 0)
        notify.assert_called_once()

    def test_existing_instance_notice_uses_localization_authority(self):
        self.assertEqual(
            main_window.existing_instance_notice("en"),
            "Codex Windows Status Pet is already running.\nClose the existing instance before launching this copy.",
        )


if __name__ == "__main__":
    unittest.main()
