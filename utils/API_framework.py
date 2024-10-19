"""
API framework abstraction module for the DataDiVR-Backend.

This module provides abstractions for web framework components to make it easy
to switch between different web frameworks. It currently wraps FastAPI components.
"""

from fastapi import APIRouter
from fastapi import HTTPException as FastAPIHTTPException
from fastapi import Query as FastAPIQuery


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
