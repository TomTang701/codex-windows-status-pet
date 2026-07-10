"""Validation rules shared by the settings UI and configuration boundary."""

from __future__ import annotations

import re

SIGNED_CANDIDATE = re.compile(r"^-?\d*$")
UNSIGNED_CANDIDATE = re.compile(r"^\d*$")
SIGNED_SUBMIT = re.compile(r"^-?\d+$")
UNSIGNED_SUBMIT = re.compile(r"^\d+$")


def is_signed_integer_candidate(value):
    return isinstance(value, str) and bool(SIGNED_CANDIDATE.fullmatch(value))


def is_unsigned_integer_candidate(value):
    return isinstance(value, str) and bool(UNSIGNED_CANDIDATE.fullmatch(value))


def parse_signed_integer(value):
    if not isinstance(value, str) or not SIGNED_SUBMIT.fullmatch(value):
        raise ValueError("expected a signed integer")
    return int(value)


def parse_unsigned_integer(value, minimum=None, maximum=None):
    if not isinstance(value, str) or not UNSIGNED_SUBMIT.fullmatch(value):
        raise ValueError("expected an unsigned integer")
    parsed = int(value)
    if minimum is not None and parsed < minimum:
        parsed = minimum
    if maximum is not None and parsed > maximum:
        parsed = maximum
    return parsed
