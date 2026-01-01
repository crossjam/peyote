"""Application directory management using platformdirs."""

from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

APP_NAME = "dev.pirateninja.peyote"
APP_AUTHOR = "pirateninja"


def get_data_dir() -> Path:
    """Get the user data directory for the application.

    This directory is used for auto-saved sketches and logs.

    Returns:
        Path to user data directory

    """
    path = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_dir() -> Path:
    """Get the user config directory for the application.

    This directory is used for configuration files including logging config.

    Returns:
        Path to user config directory

    """
    path = Path(user_config_dir(APP_NAME, APP_AUTHOR))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_sketches_dir() -> Path:
    """Get the directory for auto-saved sketches.

    Returns:
        Path to sketches directory

    """
    path = get_data_dir() / "sketches"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_log_file() -> Path:
    """Get the path to the log file.

    Returns:
        Path to log file

    """
    return get_data_dir() / "peyote-ide.log"
