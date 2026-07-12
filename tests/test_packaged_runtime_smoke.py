"""Pure checks supporting the Windows packaged-runtime lifecycle smoke."""

from __future__ import annotations

import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from packaged_runtime_smoke import pe_subsystem


class PackagedRuntimeSmokeTests(unittest.TestCase):
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
