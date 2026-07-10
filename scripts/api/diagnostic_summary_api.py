"""Safe, copyable diagnostics with an explicit sensitive-data boundary."""

from __future__ import annotations

from datetime import datetime, timezone
import platform
from pathlib import Path


def build_diagnostic_summary(
    version,
    settings_path,
    log_path,
    activity_path,
    app_server_running,
    quota_state,
    monitor_count,
    dpi,
    now=None,
):
    """Return a stable summary; never accept or serialize raw provider payloads."""
    now = now or datetime.now(timezone.utc)
    state = quota_state or "loading"
    lines = [
        "Codex Windows Status Pet diagnostics",
        f"version={version}",
        f"os={platform.system()} {platform.release()}",
        f"python={platform.python_version()}",
        f"app_server={'running' if app_server_running else 'not-started'}",
        f"quota_state={state}",
        f"monitor_count={max(0, int(monitor_count or 0))}",
        f"window_dpi={max(0, int(dpi or 0))}",
        f"activity_path_exists={Path(activity_path).exists() if activity_path else False}",
        f"settings_path={Path(settings_path) if settings_path else '<unset>'}",
        f"log_path={Path(log_path) if log_path else '<unset>'}",
        f"generated_at={now.isoformat()}",
        "sensitive_data=excluded (tokens, prompts, responses, raw quota, session contents)",
    ]
    return "\n".join(lines)
