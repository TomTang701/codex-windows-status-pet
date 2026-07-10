"""Codex session activity API, isolated from Tk and app-server code."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path


def _event_timestamp(record, fallback):
    stamp = record.get("timestamp", "")
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError):
        return fallback


def snapshot_activity(sessions: Path, stale_seconds=600, now=None):
    """Return active/recent activity while tolerating session-file races."""
    now = time.time() if now is None else now
    active = []
    recently_completed = []
    if not sessions.exists():
        return {"active": 0, "detail": "空闲", "progress": ""}

    files = []
    try:
        candidates = sessions.rglob("*.jsonl")
        for path in candidates:
            try:
                if path.is_file() and now - path.stat().st_mtime <= stale_seconds:
                    files.append(path)
            except OSError:
                continue
    except OSError:
        return {"active": 0, "detail": "空闲", "progress": "会话目录不可读"}

    for path in files:
        started = None
        completed = None
        last_phase = "思考中"
        last_event_time = 0
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as stream:
                for line in stream:
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    event_time = _event_timestamp(record, now)
                    last_event_time = max(last_event_time, event_time)
                    if record.get("type") == "event_msg":
                        event = record.get("payload", {}).get("type")
                        if event == "task_started":
                            started = event_time
                            completed = None
                            last_phase = "思考中"
                        elif event == "task_complete":
                            completed = event_time
                            last_phase = "已完成"
                    elif record.get("type") == "response_item" and started and not completed:
                        item_type = record.get("payload", {}).get("type")
                        if item_type in ("function_call", "custom_tool_call"):
                            last_phase = "调用工具"
                        elif item_type in ("function_call_output", "custom_tool_call_output"):
                            last_phase = "执行命令"
                        elif item_type == "message":
                            last_phase = "输出中"
                        elif item_type == "reasoning":
                            last_phase = "思考中"
        except OSError:
            continue

        recent_activity = max(started or 0, last_event_time)
        if started and not completed and now - recent_activity <= stale_seconds:
            active.append((last_event_time, last_phase))
        elif completed and now - completed <= 12:
            recently_completed.append(completed)

    if active:
        active.sort(reverse=True)
        _, phase = active[0]
        return {"active": len(active), "detail": phase, "progress": f"活动对话 {len(active)} 个"}
    if recently_completed:
        return {"active": 0, "detail": "已完成", "progress": "最近对话已完成"}
    return {"active": 0, "detail": "空闲", "progress": "没有活动中的对话"}
