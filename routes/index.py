"""
Index API endpoint module for the DataDiVR-Backend.

This module defines the root endpoint that serves the main HTML page.
"""

from utils.API_framework import Request, Route, Templates
from utils.custom_logging import logger

route = Route()
templates = Templates(directory="templates")


@route.get("/")
async def root(request: Request):
    """
    Serve the main HTML page using the templating engine.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered index.jinja template.
    """
    logger.debug("Serving index.jinja")
    try:
        return templates.TemplateResponse("index.jinja", {"request": request})
    except Exception as e:
        logger.error(f"Error serving index.jinja: {str(e)}")
        return f"<h1>Error: {str(e)}</h1>"
