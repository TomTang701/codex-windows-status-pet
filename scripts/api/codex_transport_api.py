"""Local Codex CLI discovery and app-server JSON-RPC transport."""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import threading
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


DEFAULT_CLIENT_VERSION = "1.1.0"


def find_codex() -> str:
    candidates = []
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured:
        candidates.append(configured)
    config = Path.home() / ".codex" / "config.toml"
    if config.exists() and tomllib:
        try:
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))

            def find_config_values(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key.lower() == "codex_cli_path" and isinstance(child, str):
                            candidates.append(child)
                        else:
                            find_config_values(child)

            find_config_values(parsed)
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            logging.getLogger("codex-status-pet").warning("unable to parse Codex config.toml", exc_info=True)
    candidates.extend(["codex.exe", "codex"])
    for candidate in candidates:
        if Path(candidate).exists():
            return str(Path(candidate))
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError("Codex CLI was not found")


class AppServer:
    def __init__(self, updates, client_version=DEFAULT_CLIENT_VERSION):
        self.updates = updates
        self.client_version = client_version
        self.proc = None
        self.next_id = 1
        self.pending = {}
        self.lock = threading.Lock()

    def start(self):
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = subprocess.SW_HIDE
        self.proc = subprocess.Popen(
            [find_codex(), "app-server", "--stdio"], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
            encoding="utf-8", startupinfo=startup,
        )
        threading.Thread(target=self._reader, name="codex-app-server-reader", daemon=True).start()
        initialized = self._send({"method": "initialize", "params": {"clientInfo": {
            "name": "codex-windows-status-pet", "title": "Codex Windows Status Pet", "version": self.client_version
        }, "capabilities": {"experimentalApi": True}}})
        if "error" in initialized:
            raise RuntimeError(initialized["error"].get("message", "Codex app-server initialization failed"))
        self._send({"method": "initialized", "params": {}}, wait=False)

    def _reader(self):
        try:
            for line in self.proc.stdout:
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ident = message.get("id")
                with self.lock:
                    callback = self.pending.pop(ident, None)
                if callback:
                    callback(message)
        finally:
            self.updates.put({"error": "Codex app-server stopped"})

    def _send(self, message, wait=True):
        if not self.proc or self.proc.poll() is not None:
            raise RuntimeError("Codex app-server is not running")
        ident = None
        if wait:
            with self.lock:
                ident = self.next_id
                self.next_id += 1
                message["id"] = ident
                event = threading.Event()
                result = []
                self.pending[ident] = lambda value: (result.append(value), event.set())
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()
        if not wait:
            return None
        if not event.wait(5):
            with self.lock:
                self.pending.pop(ident, None)
            raise TimeoutError("Codex app-server request timed out")
        return result[0]

    def read_limits(self):
        response = self._send({"method": "account/rateLimits/read", "params": {}})
        if "error" in response:
            raise RuntimeError(response["error"].get("message", "rate limit request failed"))
        return response.get("result", {})

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
