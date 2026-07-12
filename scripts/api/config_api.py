"""Configuration API: validation, normalization, and durable persistence."""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .window_scale_api import (
    DEFAULT_WINDOW_SCALE_PERCENT,
    derive_window_metrics,
    infer_scale_percent,
)


CONFIG_SCHEMA_VERSION = 1


class ConfigWriteProtectedError(OSError):
    """Raised when a routine save would destroy an unsafe source configuration."""


@dataclass(frozen=True)
class ConfigLoadResult:
    """Validated settings plus source compatibility and persistence safety."""

    settings: dict
    warnings: tuple[str, ...]
    schema_status: str
    writable: bool

    def __iter__(self):
        """Retain the historical `(settings, warnings)` unpacking API."""
        yield self.settings
        yield list(self.warnings)

DEFAULT_WINDOW_METRICS = derive_window_metrics(DEFAULT_WINDOW_SCALE_PERCENT)


DEFAULT_SETTINGS = {
    "schema_version": CONFIG_SCHEMA_VERSION,
    "alpha": 0.95,
    "font_color": "#e5e7eb",
    "font_size": DEFAULT_WINDOW_METRICS.text_font_size,
    "background_color": "#111827",
    "topmost": True,
    "locked": False,
    "x": 30,
    "y": 120,
    "window_width": DEFAULT_WINDOW_METRICS.width,
    "window_height": DEFAULT_WINDOW_METRICS.height,
    "scale_mode": "proportional",
    "window_scale_percent": DEFAULT_WINDOW_METRICS.scale_percent,
    "refresh_interval_seconds": 5,
    "compact_when_idle": False,
    "show_primary_5h": True,
    "show_weekly": True,
    "show_reset_credit": True,
    "battery_quota_source": "weekly",
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


def _valid_numeric_scale(value):
    if isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _apply_scale_compatibility(settings, scale_percent):
    metrics = derive_window_metrics(scale_percent)
    settings["window_scale_percent"] = metrics.scale_percent
    settings["font_size"] = metrics.text_font_size
    settings["window_width"] = metrics.width
    settings["window_height"] = metrics.height
    settings["scale_mode"] = "proportional"
    return metrics


def normalize_settings(raw):
    """Return validated settings and field-level warnings for malformed input."""
    settings = dict(DEFAULT_SETTINGS)
    warnings = []
    if not isinstance(raw, dict):
        return settings, ["settings root is not an object"]

    schema_version = raw.get("schema_version")
    if schema_version is not None:
        parsed_schema = _integer_value(schema_version, -1)
        if parsed_schema != CONFIG_SCHEMA_VERSION:
            return settings, [f"unsupported settings schema version: {schema_version}"]

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

    for key in (
        "topmost",
        "locked",
        "compact_when_idle",
        "show_primary_5h",
        "show_weekly",
        "show_reset_credit",
    ):
        settings[key] = _bool_value(raw.get(key, settings[key]), settings[key])
        if key in raw and settings[key] == DEFAULT_SETTINGS[key] and raw[key] not in (True, False, 0, 1, "true", "false", "1", "0", "yes", "no", "on", "off"):
            warnings.append(f"{key} is invalid; default retained")
    source = raw.get("battery_quota_source", settings["battery_quota_source"])
    if source in {"primary_5h", "weekly"}:
        settings["battery_quota_source"] = source
    elif "battery_quota_source" in raw:
        warnings.append("battery_quota_source is invalid; weekly retained")
    if "window_scale_percent" in raw:
        candidate = raw.get("window_scale_percent")
        if _valid_numeric_scale(candidate):
            scale_percent = candidate
        else:
            scale_percent = DEFAULT_WINDOW_SCALE_PERCENT
            warnings.append("window_scale_percent is invalid; default retained")
    else:
        scale_percent = infer_scale_percent(settings["window_width"], settings["window_height"])
    _apply_scale_compatibility(settings, scale_percent)
    return settings, warnings


def load_settings(path: Path):
    """Load settings without allowing a malformed file to crash the app."""
    warnings = []
    try:
        # Windows editors and PowerShell may write a UTF-8 BOM.
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        raw = {}
        schema_status = "missing"
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raw = {}
        warnings.append(f"settings file could not be read: {exc}")
        schema_status = "malformed"
    else:
        if not isinstance(raw, dict):
            schema_status = "malformed"
        elif "schema_version" not in raw:
            schema_status = "legacy"
        elif _integer_value(raw.get("schema_version"), -1) == CONFIG_SCHEMA_VERSION:
            schema_status = "current"
        else:
            schema_status = "unsupported"
    settings, normalize_warnings = normalize_settings(raw)
    combined = tuple(warnings + normalize_warnings)
    return ConfigLoadResult(
        settings=settings,
        warnings=combined,
        schema_status=schema_status,
        writable=schema_status in {"missing", "legacy", "current"} and not combined,
    )


def save_settings_atomic(path: Path, settings, *, allow_unsafe_overwrite=False):
    """Write settings atomically and retain one previous valid file as a backup."""
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = backup_settings_path(path)
    if path.exists():
        source = load_settings(path)
        if not source.writable and not allow_unsafe_overwrite:
            raise ConfigWriteProtectedError(
                f"settings write blocked: source status is {source.schema_status}"
            )
        if source.writable:
            _copy_atomic(path, backup)
    persisted = dict(settings)
    persisted["schema_version"] = CONFIG_SCHEMA_VERSION
    payload = json.dumps(persisted, ensure_ascii=False, indent=2) + "\n"
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
    result = load_settings(backup)
    if not result.writable:
        return False
    payload = json.dumps(result.settings, ensure_ascii=False, indent=2) + "\n"
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
