"""
Custom logging configuration module for the DataDiVR-Backend.

This module provides a function to configure colorful logging for the DataDiVR-Backend
application with timestamps for all log levels.
"""

import logging

import colorlog


def configure_logging():
    """
    Configure colorful logging for the DataDiVR-Backend with timestamps for all levels.

    This function sets up a colorlog logger with custom formatting and color schemes
    for different log levels. It configures the root logger to use this setup.

    Returns:
        logging.Logger: The configured root logger with colorful output.
    """
    # Create a color formatter
    formatter = colorlog.ColoredFormatter(
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

    # Get the root logger
    logger = colorlog.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a stream handler and set the formatter
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


# Create a global logger instance
logger = configure_logging()
