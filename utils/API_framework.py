"""Asbstraction of web framework.

We do this to make it easy to switch between different web frameworks.
So for example things like routes/sum.py does not need to know what
web framework we are using, it can just use the functions and classes
from this module and we can easily swap it out.
"""

from fastapi import APIRouter
from fastapi import HTTPException as FastAPIHTTPException
from fastapi import Query as FastAPIQuery


class Route(APIRouter):
    """Wrapper class for APIRouter to abstract web framework specifics."""

    pass


Query = FastAPIQuery
HTTPException = FastAPIHTTPException
