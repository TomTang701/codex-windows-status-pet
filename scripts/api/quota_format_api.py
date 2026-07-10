"""Pure formatting helpers for quota display."""

from __future__ import annotations

from datetime import datetime, timezone


def _epoch(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            try:
                normalized = value.replace("Z", "+00:00")
                parsed = datetime.fromisoformat(normalized)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed.timestamp()
            except ValueError:
                return None
    return None


def _local_datetime(value):
    """Return a local datetime for an approved timestamp value, or None."""
    if value in (None, ""):
        return None
    timestamp = _epoch(value)
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(timestamp).astimezone()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def local_time_only(value) -> str:
    """Return local ``HH:MM`` for a timestamp, or a safe placeholder."""
    current = _local_datetime(value)
    if current is None:
        return "--"
    return f"{current.hour:02d}:{current.minute:02d}"


def local_time_date(value) -> str:
    """Return local ``HH:MM M/D`` without platform-specific directives."""
    current = _local_datetime(value)
    if current is None:
        return "--"
    return f"{current.hour:02d}:{current.minute:02d} {current.month}/{current.day}"


def earliest_future_expiry(expirations, now=None):
    """Return the earliest future epoch from a mixed provider response."""
    current = datetime.now().timestamp() if now is None else float(now)
    values = []
    def candidates(value):
        if isinstance(value, dict):
            for key in ("expiresAt", "resetsAt", "resetAt"):
                if key in value:
                    yield value[key]
            for child in value.values():
                yield from candidates(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                yield from candidates(child)
        else:
            yield value

    for value in candidates(expirations):
        timestamp = _epoch(value)
        if timestamp is None:
            continue
        if timestamp > current:
            values.append(timestamp)
    return min(values) if values else None


def quota_line(label, value, reset_at):
    suffix = local_time_date(reset_at) if reset_at else "--"
    return f"{label} {value} / {suffix}"


def reset_credit_line(count, expiration) -> str:
    formatted = local_time_date(expiration)
    if formatted == "--":
        return f"重置 {count} 次"
    return f"重置 {count} 次 / {formatted}"
