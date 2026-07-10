"""Typed quota-domain values shared by providers and state management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UsageWindow:
    remaining_percent: float | None
    resets_at: datetime | None


@dataclass(frozen=True)
class ResetCreditSummary:
    available_count: int | None
    expirations: tuple[datetime, ...] = ()
    earliest_future_expiration: datetime | None = None


@dataclass(frozen=True)
class QuotaSnapshot:
    status: str
    primary: UsageWindow | None
    weekly: UsageWindow | None
    reset_credits: ResetCreditSummary
    fetched_at: datetime
    error_code: str | None = None
