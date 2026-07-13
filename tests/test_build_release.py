"""Release builder fails before PyInstaller when a project staging path is in use."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import build_release


class BuildReleaseTests(unittest.TestCase):
    def test_clean_build_paths_fails_clearly_when_release_staging_remains(self):
        with tempfile.TemporaryDirectory() as directory:
            staging = Path(directory) / "release"
            staging.mkdir()
            with mock.patch.object(build_release.shutil, "rmtree"):
                with self.assertRaisesRegex(RuntimeError, "staging path is in use"):
                    build_release.clean_build_paths((staging,))


if __name__ == "__main__":
    unittest.main()
