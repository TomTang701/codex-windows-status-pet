import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.codex_transport_api import AppServer, find_codex


class CodexTransportTests(unittest.TestCase):
    def test_discovery_honors_configured_existing_cli_path(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "codex.exe"
            candidate.write_text("placeholder", encoding="utf-8")
            with mock.patch.dict(os.environ, {"CODEX_CLI_PATH": str(candidate)}):
                self.assertEqual(find_codex(), str(candidate))

    def test_transport_starts_with_empty_pending_state(self):
        server = AppServer([])
        self.assertIsNone(server.proc)
        self.assertEqual(server.pending, {})
        self.assertEqual(server.client_version, "0.2.1")

    def test_send_rejects_stopped_process(self):
        server = AppServer([])
        with self.assertRaises(RuntimeError):
            server._send({"method": "test"})
