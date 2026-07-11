"""Stable row identities for overlay presentation text."""

from __future__ import annotations

from dataclasses import dataclass


ROW_IDS = ("activity", "progress", "primary_5h", "weekly", "reset_credit")


@dataclass(frozen=True)
class StatusRowsSnapshot:
    activity: str
    progress: str
    primary_5h: str
    weekly: str
    reset_credit: str

    def as_dict(self) -> dict[str, str]:
        return {row_id: getattr(self, row_id) for row_id in ROW_IDS}

    def as_text(self) -> str:
        return "\n".join(self.as_dict().values())


def split_status_text(text) -> StatusRowsSnapshot:
    """Normalize legacy multiline presentation into exactly five stable rows."""
    lines = str(text or "").splitlines()
    lines = (lines + [""] * len(ROW_IDS))[: len(ROW_IDS)]
    return StatusRowsSnapshot(*lines)
