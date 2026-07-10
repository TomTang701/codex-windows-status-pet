"""Configuration API: validation, normalization, and durable persistence."""

from __future__ import annotations

import json
import os
import re
import shutil
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
    "window_width": 330,
    "window_height": 138,
    "scale_mode": "free",
    "refresh_interval_seconds": 5,
    "compact_when_idle": False,
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


def _integer_value(value, default, minimum=None, maximum=None):
    """Parse an integer without accepting floats or embedded punctuation."""
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        result = value
    elif isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value.strip()):
        result = int(value.strip())
    else:
        return default
    if minimum is not None:
        result = max(minimum, result)
    if maximum is not None:
        result = min(maximum, result)
    return result


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
        value = raw.get(key, settings[key])
        parsed = _integer_value(value, settings[key])
        if parsed == settings[key] and value != settings[key]:
            warnings.append(f"{key} is invalid; default retained")
        settings[key] = parsed

    for key, minimum, maximum in (("window_width", 180, 1200), ("window_height", 80, 800)):
        value = raw.get(key, settings[key])
        parsed = _integer_value(value, settings[key], minimum, maximum)
        if parsed == settings[key] and value != settings[key]:
            warnings.append(f"{key} is invalid; default retained")
        settings[key] = parsed

    scale_mode = raw.get("scale_mode", settings["scale_mode"])
    if scale_mode in {"free", "proportional"}:
        settings["scale_mode"] = scale_mode
    elif "scale_mode" in raw:
        warnings.append("scale_mode is invalid; default retained")

    value = raw.get("refresh_interval_seconds", settings["refresh_interval_seconds"])
    parsed = _integer_value(value, settings["refresh_interval_seconds"], 1, 10)
    if parsed == settings["refresh_interval_seconds"] and value != settings["refresh_interval_seconds"]:
        warnings.append("refresh_interval_seconds is invalid; default retained")
    settings["refresh_interval_seconds"] = parsed

    for key in ("topmost", "locked", "compact_when_idle"):
        settings[key] = _bool_value(raw.get(key, settings[key]), settings[key])
        if key in raw and settings[key] == DEFAULT_SETTINGS[key] and raw[key] not in (True, False, 0, 1, "true", "false", "1", "0", "yes", "no", "on", "off"):
            warnings.append(f"{key} is invalid; default retained")
    return settings, warnings


def load_settings(path: Path):
    """Load settings without allowing a malformed file to crash the app."""
    warnings = []
    try:
        # Windows editors and PowerShell may write a UTF-8 BOM.
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        raw = {}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raw = {}
        warnings.append(f"settings file could not be read: {exc}")
    settings, normalize_warnings = normalize_settings(raw)
    return settings, warnings + normalize_warnings


def save_settings_atomic(path: Path, settings):
    """Write settings atomically and retain one previous valid file as a backup."""
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = backup_settings_path(path)
    if path.exists():
        _, warnings = load_settings(path)
        if not warnings:
            _copy_atomic(path, backup)
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


def backup_settings_path(path: Path) -> Path:
    """Return the sidecar path for the last settings file."""
    return path.with_name(path.name + ".bak")


def _copy_atomic(source: Path, target: Path):
    """Copy a known file to a same-directory target without partial output."""
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    os.close(fd)
    try:
        shutil.copyfile(source, temporary)
        with open(temporary, "rb+") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def restore_settings_backup(path: Path) -> bool:
    """Restore the validated sidecar backup, returning False when unavailable or malformed."""
    backup = backup_settings_path(path)
    if not backup.exists():
        return False
    settings, warnings = load_settings(backup)
    if warnings:
        return False
    payload = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_name(f".{path.name}.restore.tmp")
    try:
        temporary.write_text(payload, encoding="utf-8", newline="\n")
        with temporary.open("rb+") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        return True
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
