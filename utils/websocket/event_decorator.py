"""
Event decorator module for WebSocket event handling in the DataDiVR-Backend.

This module provides a decorator function for registering event handlers
in the DataDiVR-Backend WebSocket system.
"""

import inspect
from functools import wraps
from typing import Any, Callable, Dict

from fastapi import WebSocket


def event_decorator(handlers: Dict[str, Callable], get_client_info: Callable):
    """
    Create a decorator for registering WebSocket event handlers.

    This function returns a decorator that can be used to register functions
    as handlers for specific WebSocket events. The decorator also wraps the
    handler function to provide it with appropriate arguments based on its
    signature.

    Args:
        handlers (Dict[str, Callable]): A dictionary to store event handlers.
        get_client_info (Callable): A function to retrieve client information.

    Returns:
        Callable: A decorator function for registering event handlers.
    """

    def decorator(event_name: str):
        """
        Decorator for registering a function as a handler for a specific event.

        Args:
            event_name (str): The name of the event to handle.

        Returns:
            Callable: A wrapper function that registers and wraps the handler.
        """

        def wrapper(func: Callable):
            """
            Wrapper function that registers the handler and wraps it to provide appropriate arguments.

            Args:
                func (Callable): The event handler function to be wrapped and registered.

            Returns:
                Callable: The wrapped event handler function.
            """

            @wraps(func)
            async def inner(data: Dict[Any, Any], websocket: WebSocket):
                """
                Inner function that calls the event handler with appropriate arguments.

                This function inspects the handler's signature and calls it with the
                arguments it expects, which may include 'data', 'websocket', and 'client_info'.

                Args:
                    data (Dict[Any, Any]): The event data.
                    websocket (WebSocket): The WebSocket connection.

                Returns:
                    Any: The return value of the event handler function.
                """
                client_info = get_client_info(websocket)
                sig = inspect.signature(func)
                params = {
                    param: value
                    for param, value in {
                        "data": data,
                        "websocket": websocket,
                        "client_info": client_info,
                    }.items()
                    if param in sig.parameters
                }
                return await func(**params)

            handlers[event_name] = inner
            return func

        return wrapper

    return decorator
