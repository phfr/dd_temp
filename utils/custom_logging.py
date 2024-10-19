"""Logging configuration module for the application."""

import logging

import colorlog


def configure_logging():
    """Configure colorful logging for the application with timestamps for all levels."""
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


logger = configure_logging()
