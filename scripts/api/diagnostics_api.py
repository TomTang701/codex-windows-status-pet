"""Diagnostics API used when the app runs without a console."""

from __future__ import annotations

import logging
import sys
import threading
from pathlib import Path


def configure_logging(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(threadName)s %(message)s",
        encoding="utf-8",
    )

    def report_exception(exc_type, exc_value, exc_traceback):
        logging.getLogger("codex-status-pet").critical(
            "uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = report_exception

    def report_thread_exception(args):
        logging.getLogger("codex-status-pet").critical(
            "thread exception in %s", args.thread.name if args.thread else "unknown", exc_info=(args.exc_type, args.exc_value, args.exc_traceback)
        )

    threading.excepthook = report_thread_exception
    return logging.getLogger("codex-status-pet")
