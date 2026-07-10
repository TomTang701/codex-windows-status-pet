"""Validate declared runtime dependencies against the active Python environment."""

from __future__ import annotations

from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENT = re.compile(r"^([A-Za-z0-9_.-]+)\s*>=\s*(\d+(?:\.\d+)*)$")
IMPORT_NAMES = {"pillow": "PIL", "pystray": "pystray"}


def _version_tuple(value):
    return tuple(int(part) for part in value.split("."))


def check(root: Path = ROOT):
    errors = []
    requirements = (root / "requirements.txt").read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(requirements, 1):
        text = line.split("#", 1)[0].strip()
        if not text:
            continue
        match = REQUIREMENT.fullmatch(text)
        if not match:
            errors.append(f"requirements.txt:{line_number}: unsupported requirement: {text}")
            continue
        package, minimum = match.groups()
        try:
            installed = version(package)
        except PackageNotFoundError:
            errors.append(f"missing dependency: {package}")
            continue
        try:
            if _version_tuple(installed) < _version_tuple(minimum):
                errors.append(f"dependency below minimum: {package}={installed} < {minimum}")
        except ValueError:
            errors.append(f"unparseable installed version: {package}={installed}")
        import_name = IMPORT_NAMES.get(package.lower(), package)
        try:
            import_module(import_name)
        except Exception as exc:
            errors.append(f"dependency import failed: {package} ({type(exc).__name__})")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("runtime dependencies passed")
