"""Validate the required packaged-runtime screenshot evidence set."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "zh-CN")
VIEWS = ("main-overlay", "context-menu", "settings")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def expected_paths():
    return {
        Path("docs") / "assets" / "readme" / language / f"{view}.png"
        for language in LANGUAGES
        for view in VIEWS
    }


def check(root=ROOT):
    """Return all evidence errors without accepting placeholder or mislinked files."""
    root = Path(root)
    expected = expected_paths()
    assets = root / "docs" / "assets" / "readme"
    actual = {
        path.relative_to(root)
        for path in assets.rglob("*.png")
    } if assets.exists() else set()
    errors = []
    for path in sorted(expected - actual):
        errors.append(f"missing screenshot: {path.as_posix()}")
    for path in sorted(actual - expected):
        errors.append(f"unexpected screenshot: {path.as_posix()}")
    for path in sorted(actual & expected):
        if not (root / path).read_bytes().startswith(PNG_SIGNATURE):
            errors.append(f"screenshot is not PNG: {path.as_posix()}")

    readmes = {"README.md": "en", "README.zh-CN.md": "zh-CN"}
    for name, language in readmes.items():
        try:
            text = (root / name).read_text(encoding="utf-8")
        except OSError:
            errors.append(f"missing README: {name}")
            continue
        own = {path.as_posix() for path in expected if path.parts[3] == language}
        other = {path.as_posix() for path in expected if path.parts[3] != language}
        for path in sorted(own):
            if path not in text:
                errors.append(f"{name} does not reference screenshot: {path}")
        for path in sorted(other):
            if path in text:
                errors.append(f"{name} references wrong-language screenshot: {path}")
    return errors


def main():
    errors = check()
    if errors:
        raise SystemExit("\n".join(errors))
    print("README screenshot evidence passed")


if __name__ == "__main__":
    main()
