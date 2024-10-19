"""
Custom logging configuration module for the DataDiVR-Backend.

This module provides a function to configure colorful logging for the DataDiVR-Backend
application with timestamps for all log levels, outputting to both console and file.
"""

import logging
import os
from datetime import datetime

import colorlog


def configure_logging():
    """
    Configure colorful logging for the DataDiVR-Backend with timestamps for all levels.

    This function sets up a colorlog logger with custom formatting and color schemes
    for different log levels. It configures the root logger to use this setup and
    outputs logs to both console and a file in the logs/ directory.

    Returns:
        logging.Logger: The configured root logger with colorful output.
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Create a color formatter for console output
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    # Create a formatter for file output (without colors)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Get the root logger
    logger = colorlog.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a stream handler for console output and set the formatter
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Create a file handler for file output
    current_day = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(logs_dir, f"datadivr_backend_{current_day}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create a global logger instance
logger = configure_logging()
