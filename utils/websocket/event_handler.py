"""
Event handling module for WebSocket connections in the DataDiVR-Backend.

This module provides an EventHandler class to manage and execute event handlers
for different WebSocket events in the DataDiVR-Backend system.
"""

import time
from typing import Any, Callable, Dict

from fastapi import WebSocket

from ..custom_logging import logger


class EventHandler:
    """
    Manages and executes event handlers for WebSocket events in the DataDiVR-Backend.

    This class maintains a dictionary of event handlers and provides methods to
    handle incoming WebSocket events, either by executing a registered handler
    or by broadcasting unknown events to all clients.
    """

    def __init__(
        self,
        handlers: Dict[str, Callable],
        get_client_info: Callable,
        broadcast: Callable,
    ):
        """
        Initialize the EventHandler with event handlers and utility functions.

        Args:
            handlers (Dict[str, Callable]): A dictionary mapping event names to their handler functions.
            get_client_info (Callable): A function to retrieve client information given a WebSocket.
            broadcast (Callable): A function to broadcast messages to all clients.
        """
        self.handlers = handlers
        self.get_client_info = get_client_info
        self.broadcast_func = broadcast

    async def handle_event(
        self, event_name: str, data: Dict[Any, Any], websocket: WebSocket
    ):
        """
        Handle an incoming WebSocket event.

        This method either executes a registered handler for the event or
        broadcasts the event to all clients if no handler is found.

        Args:
            event_name (str): The name of the event to handle.
            data (Dict[Any, Any]): The data associated with the event.
            websocket (WebSocket): The WebSocket connection that received the event.
        """
        client_info = self.get_client_info(websocket)
        client_id, client_name = client_info["client_id"], client_info["first_name"]

        logger.debug(
            "Received event: %s with data: %s from client %s (%s)",
            event_name,
            data,
            client_id,
            client_name,
        )

        # if we have an event handler for this event, execute it
        # otherwise, broadcast the event to all clients except the sender
        if event_name in self.handlers:
            start_time = time.time()
            await self.handlers[event_name](data, websocket)
            duration = time.time() - start_time
            logger.debug(
                "Event handler '%s' took %.5f seconds to execute", event_name, duration
            )
        else:
            logger.debug(
                "Unknown event received: %s from client %s. Broadcasting to all clients except sender.",
                event_name,
                client_name,
            )
            await self.broadcast_func(
                {
                    "event": event_name,
                    "sender_id": client_id,
                    "sender_name": client_name,
                    "data": data,
                }
            )

    def register_handler(self, event_name: str, handler: Callable):
        """
        Register a new event handler.

        Args:
            event_name (str): The name of the event to handle.
            handler (Callable): The function to handle the event.
        """
        self.handlers[event_name] = handler
        logger.debug("Registered new handler for event: %s", event_name)

    def remove_handler(self, event_name: str):
        """
        Remove an event handler.

        Args:
            event_name (str): The name of the event whose handler should be removed.
        """
        if event_name in self.handlers:
            del self.handlers[event_name]
            logger.debug("Removed handler for event: %s", event_name)
        else:
            logger.warning(
                "Attempted to remove non-existent handler for event: %s", event_name
            )
