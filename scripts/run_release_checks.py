"""Backward-compatible alias for the non-strict daily quality gate."""

from run_quality_checks import main


if __name__ == "__main__":
    raise SystemExit(main())
