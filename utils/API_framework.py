"""
API framework abstraction module for the DataDiVR-Backend.

This module provides abstractions for web framework components to make it easy
to switch between different web frameworks. It currently wraps FastAPI components.
"""

from fastapi import APIRouter
from fastapi import HTTPException as FastAPIHTTPException
from fastapi import Query as FastAPIQuery
from fastapi import Request as FastAPIRequest
from fastapi.responses import HTMLResponse as FastAPIHTMLResponse
from fastapi.templating import Jinja2Templates


class Route(APIRouter):
    """
    Wrapper class for APIRouter to abstract web framework specifics.

    This class inherits from FastAPI's APIRouter and can be extended
    to add DataDiVR-Backend specific functionality if needed.
    """

    pass


# Alias FastAPI's Query to our framework's Query
Query = FastAPIQuery

# Alias FastAPI's HTTPException to our framework's HTTPException
HTTPException = FastAPIHTTPException

# Alias FastAPI's HTMLResponse to our framework's HTMLResponse
HTMLResponse = FastAPIHTMLResponse

# Alias FastAPI's Request to our framework's Request
Request = FastAPIRequest


# Create a wrapper class for templating
class Templates:
    """
    Wrapper class for templating engine to abstract template rendering specifics.
    """

    def __init__(self, directory: str):
        self._engine = Jinja2Templates(directory=directory)

    def TemplateResponse(self, name: str, context: dict, status_code: int = 200):
        """
        Render a template with the given context.

        Args:
            name (str): The name of the template file.
            context (dict): The context data to be passed to the template.
            status_code (int, optional): The HTTP status code. Defaults to 200.

        Returns:
            TemplateResponse: The rendered template response.
        """
        return self._engine.TemplateResponse(name, context, status_code=status_code)
