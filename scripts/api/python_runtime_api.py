"""Python interpreter discovery and validation for source deployment."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys


@dataclass(frozen=True)
class RuntimeProbe:
    path: Path
    source: str
    version: tuple[int, int]
    bits: int
    tkinter: bool
    pip: bool
    pythonw: Path | None

    @property
    def compatible(self):
        return self.version >= (3, 10) and self.bits == 64 and self.tkinter and self.pip and self.pythonw is not None


PROBE = (
    "import json, struct, sys\n"
    "payload = {'path': sys.executable, 'version': [sys.version_info.major, sys.version_info.minor], "
    "'bits': struct.calcsize('P') * 8}\n"
    "try:\n import tkinter; payload['tkinter'] = True\n"
    "except Exception:\n payload['tkinter'] = False\n"
    "try:\n import pip; payload['pip'] = True\n"
    "except Exception:\n payload['pip'] = False\n"
    "print(json.dumps(payload))"
)


def probe_runtime(command, *, source="unknown", runner=subprocess.run):
    command = [str(part) for part in (command if isinstance(command, (list, tuple)) else [command])]
    try:
        result = runner(command + ["-c", PROBE], capture_output=True, text=True, check=False)
        payload = json.loads(result.stdout.strip())
        path = Path(payload["path"])
        pythonw = path.with_name("pythonw.exe")
        if not pythonw.is_file():
            pythonw = None
        return RuntimeProbe(
            path=path,
            source=source,
            version=tuple(payload["version"]),
            bits=int(payload["bits"]),
            tkinter=bool(payload["tkinter"]),
            pip=bool(payload["pip"]),
            pythonw=pythonw,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError, TypeError):
        return None


def runtime_commands(*, codex_python=None, py_launcher="py.exe", path_python="python.exe"):
    commands = []
    if codex_python:
        commands.append(("codex", [codex_python]))
    if shutil.which(py_launcher) or Path(py_launcher).exists():
        commands.append(("py", [py_launcher, "-3"]))
    if shutil.which(path_python) or Path(path_python).exists():
        commands.append(("path", [path_python]))
    return commands


def choose_runtime(sources, *, codex_python=None, py_launcher="py.exe", path_python="python.exe"):
    candidates = runtime_commands(
        codex_python=codex_python,
        py_launcher=py_launcher,
        path_python=path_python,
    )
    by_source = {source: command for source, command in candidates}
    errors = []
    for source in sources:
        command = by_source.get(source, [source])
        probe = probe_runtime(command, source=source)
        if probe is None:
            errors.append(f"{source}: interpreter could not be probed")
        elif probe.compatible:
            return probe
        else:
            errors.append(f"{source}: Python 3.10+, 64-bit, Tkinter, pip, and pythonw.exe are required")
    raise RuntimeError("No compatible Python 3.10+ runtime found: " + "; ".join(errors))
