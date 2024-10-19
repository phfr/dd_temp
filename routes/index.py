"""
Index API endpoint module for the DataDiVR-Backend.

This module defines the root endpoint that serves the main HTML page.
"""

from utils.API_framework import HTMLResponse, Route
from utils.custom_logging import logger

route = Route()


@route.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the main HTML page.

    Returns:
        str: The content of the index.html file.
    """
    logger.debug("Serving index.html")
    try:
        with open("templates/index.html", "r") as f:
            content = f.read()
        logger.info("Successfully served index.html")
        return content
    except FileNotFoundError:
        logger.error("index.html not found in templates directory")
        return "<h1>Error: index.html not found</h1>"
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return f"<h1>Error: {str(e)}</h1>"
