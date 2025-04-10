"""Logging configuration for geoterminal."""

import sys
from loguru import logger


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging based on the log level.

    Args:
        log_level: The log level to use (default: INFO)
    """
    # Remove default handler
    logger.remove()

    # Format based on log level
    if log_level == "DEBUG":
        # Debug format includes timestamp and file
        fmt = ("{time:YYYY-MM-DD HH:mm:ss} | "
               "{file}:{line} | {level} | {message}")
    else:
        # Info format is minimal
        fmt = "{message}"

    # Add handler with appropriate format
    logger.add(
        sys.stderr,
        format=fmt,
        level=log_level,
        filter=lambda record: (
            # Show all logs at INFO and above
            record["level"].no >= logger.level("INFO").no
            # Show geometry and h3 operations only in DEBUG
            or (
                log_level == "DEBUG"
                and record["file"].name in ["geometry_operations.py", "h3_operations.py"]
            )
        )
    )
