"""Logging configuration for the IDE."""

from pathlib import Path

from loguru import logger

from .app_dirs import get_config_dir, get_log_file


def setup_logging() -> None:
    """Set up logging for the IDE application.

    Creates a default logging configuration if none exists,
    then configures loguru for file and console logging.
    """
    log_file = get_log_file()

    # Configure loguru with file and console logging
    logger.add(
        str(log_file),
        level="INFO",
        rotation="10 MB",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    # Set debug level for IDE modules
    logger.level("peyote.ide", "DEBUG")

    logger.info(f"Logging initialized. Log file: {log_file}")
