"""Structured logging setup without logging sensitive configuration values."""

import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def configure_logging(log_level: str) -> None:
    """Configure JSON logs once for API and worker processes."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.upper())

    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s")
    )
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module logger configured by the application factory."""
    return logging.getLogger(name)
