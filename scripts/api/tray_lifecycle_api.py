"""Deterministic tray action and recovery policy."""

from __future__ import annotations


TRAY_ACTIONS = frozenset({"show", "hide", "settings", "tray_menu", "exit", "tray_error"})


def is_known_action(action):
    return isinstance(action, str) and action in TRAY_ACTIONS


def requires_visible_overlay(action):
    return action in {"show", "settings", "tray_menu"}


def should_schedule_restart(action, already_scheduled=False, closing=False):
    return action == "tray_error" and not already_scheduled and not closing
