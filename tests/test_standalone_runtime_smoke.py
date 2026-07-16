"""Contracts for the direct-use Standalone runtime smoke."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))


class StandaloneRuntimeSmokeTests(unittest.TestCase):
    def test_direct_smoke_uses_the_standalone_channel_without_python_path(self):
        import standalone_runtime_smoke as smoke

        self.assertEqual(smoke.STANDALONE_CHANNEL, "standalone")
        environment = smoke.standalone_environment({"PATH": "ignored", "PYTHONHOME": "ignored", "PYTHONPATH": "ignored"})
        self.assertNotIn("PYTHONHOME", environment)
        self.assertNotIn("PYTHONPATH", environment)
        self.assertNotIn("Python", environment["PATH"])


if __name__ == "__main__":
    unittest.main()
