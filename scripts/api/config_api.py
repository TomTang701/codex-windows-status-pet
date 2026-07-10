"""Configuration API: validation, normalization, and durable persistence."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path


DEFAULT_SETTINGS = {
    "alpha": 0.95,
    "font_color": "#e5e7eb",
    "font_size": 10,
    "background_color": "#111827",
    "topmost": True,
    "locked": False,
    "x": 30,
    "y": 120,
}


def _bool_value(value, default):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "on"}:
            return True
        if normalized in {"false", "0", "no", "off"}:
            return False
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    return default


def normalize_settings(raw):
    """Return validated settings and field-level warnings for malformed input."""
    settings = dict(DEFAULT_SETTINGS)
    warnings = []
    if not isinstance(raw, dict):
        return settings, ["settings root is not an object"]

    for key in ("font_color", "background_color"):
        value = raw.get(key, settings[key])
        if isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value.strip()):
            settings[key] = value.strip()
        elif key in raw:
            warnings.append(f"{key} is invalid; default retained")

    try:
        settings["alpha"] = min(1.0, max(0.25, float(raw.get("alpha", settings["alpha"]))))
    except (TypeError, ValueError):
        warnings.append("alpha is invalid; default retained")

    try:
        settings["font_size"] = min(20, max(8, int(raw.get("font_size", settings["font_size"]))))
    except (TypeError, ValueError):
        warnings.append("font_size is invalid; default retained")

    for key in ("x", "y"):
        try:
            settings[key] = int(raw.get(key, settings[key]))
        except (TypeError, ValueError):
            warnings.append(f"{key} is invalid; default retained")

    for key in ("topmost", "locked"):
        settings[key] = _bool_value(raw.get(key, settings[key]), settings[key])
        if key in raw and settings[key] == DEFAULT_SETTINGS[key] and raw[key] not in (True, False, 0, 1, "true", "false", "1", "0", "yes", "no", "on", "off"):
            warnings.append(f"{key} is invalid; default retained")
    return settings, warnings


def load_settings(path: Path):
    """Load settings without allowing a malformed file to crash the app."""
    warnings = []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raw = {}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raw = {}
        warnings.append(f"settings file could not be read: {exc}")
    settings, normalize_warnings = normalize_settings(raw)
    return settings, warnings + normalize_warnings


def save_settings_atomic(path: Path, settings):
    """Write settings atomically in the target directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
