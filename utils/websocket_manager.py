"""WebSocket event management and client connection utilities.

We are abstracting away in this case fastapi. so that we can easily
switch between different web frameworks and so that the event handlers
in handlers/ do not need to know or care about the framework.
"""

import inspect
import random
import time
import uuid
from functools import wraps
from typing import Any, Callable, Dict

from fastapi import WebSocket

from utils.custom_logging import logger


class WebSocketManager:
    """Manages WebSocket events, handlers, and client connections."""

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.connected_clients: Dict[str, Dict[str, Any]] = {}
        self.first_names = [
            "Gerry",
            "Rambo",
            "Katze",
            "Peter",
            "Johnny",
            "Frank",
            "Arnold",
            "Hans",
            "Ivy",
            "Jack",
            "Kate",
            "Liam",
            "Mia",
            "Noah",
            "Olivia",
            "Gonzales",
        ]

    def get_client_info(self, websocket: WebSocket) -> Dict[str, Any]:
        """Get client information based on the WebSocket connection."""
        client_id = next(
            (
                id
                for id, info in self.connected_clients.items()
                if info["websocket"] == websocket
            ),
            None,
        )
        if client_id:
            return {
                "client_id": client_id,
                "first_name": self.connected_clients[client_id]["first_name"],
            }
        return {"client_id": None, "first_name": None}

    def event(self, event_name: str):
        """
        Decorator to register event handlers with optional client info and websocket.

        This decorator allows for flexible event handler registration, automatically
        injecting relevant parameters based on the handler's signature.

        Parameters:
        -----------
        event_name : str
            The name of the event to be handled.

        Returns:
        --------
        callable
            A decorator function that wraps the event handler.

        Usage:
        ------
        @ws_manager.event("message")
        async def handle_message(data: Dict[Any, Any], client_info: Dict[str, Any]):
            # Handler implementation

        The decorated function can have any combination of the following parameters:
        - data: Dict[Any, Any] - The event data
        - websocket: WebSocket - The WebSocket connection object
        - client_info: Dict[str, Any] - Information about the client

        The wrapper will automatically pass only the parameters that the handler function expects.

        Notes:
        ------
        - The handler is stored in the WebSocketManager's handlers dictionary.
        - The wrapper uses introspection to determine which parameters to pass to the handler.
        """

        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(data: Dict[Any, Any], websocket: WebSocket):
                client_info = self.get_client_info(websocket)
                sig = inspect.signature(func)
                params = {}

                if "data" in sig.parameters:
                    params["data"] = data
                if "websocket" in sig.parameters:
                    params["websocket"] = websocket
                if "client_info" in sig.parameters:
                    params["client_info"] = client_info

                return await func(**params)

            self.handlers[event_name] = wrapper
            return func

        return decorator

    async def handle_event(
        self, event_name: str, data: Dict[Any, Any], websocket: WebSocket
    ):
        """Handle incoming WebSocket events by calling the appropriate registered handler."""
        client_id = next(
            (
                id
                for id, info in self.connected_clients.items()
                if info["websocket"] == websocket
            ),
            None,
        )
        client_name = (
            self.connected_clients[client_id]["first_name"] if client_id else "Unknown"
        )

        logger.debug(
            "Received event: %s with data: %s from client %s (%s)",
            event_name,
            data,
            client_id,
            client_name,
        )

        # check if there is a handler for the event
        # other
        if event_name in self.handlers:
            start_time = time.time()
            await self.handlers[event_name](data, websocket)
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(
                "Event handler '%s' took %.4f seconds to execute", event_name, duration
            )
        else:
            logger.debug(
                "Unknown event received: %s from client %s (%s). Broadcasting to all clients except sender.",
                event_name,
                client_id,
                client_name,
            )
            await self.broadcast(
                {
                    "event": event_name,
                    "sender_id": client_id,
                    "sender_name": client_name,
                    "data": data,
                }
            )

    def add_client(self, client: WebSocket) -> str:
        """Add a client to the dictionary of connected clients."""
        client_id = str(uuid.uuid4())
        first_name = self._get_unique_first_name()
        self.connected_clients[client_id] = {
            "websocket": client,
            "first_name": first_name,
        }
        logger.info("New client connected. ID: %s, Name: %s", client_id, first_name)
        logger.debug("Total connected clients: %d", len(self.connected_clients))
        return client_id

    def remove_client(self, client_id: str):
        """Remove a client from the dictionary of connected clients."""
        if client_id in self.connected_clients:
            first_name = self.connected_clients[client_id]["first_name"]
            del self.connected_clients[client_id]
            logger.info("Client disconnected. ID: %s, Name: %s", client_id, first_name)
            logger.debug("Total connected clients: %d", len(self.connected_clients))
        else:
            logger.warning("Attempted to remove non-existent client. ID: %s", client_id)

    async def broadcast(self, data: Dict[Any, Any], include_sender: bool = False):
        """
        Broadcast data to connected clients.

        Args:
            data (Dict[Any, Any]): The data to broadcast.
            include_sender (bool, optional): If True, send to all clients including the sender. Defaults to False.
        """
        sender_id = data.get("sender_id")

        if include_sender:
            logger.debug(
                "Broadcasting to all %d clients. Data: %s",
                len(self.connected_clients),
                data,
            )
        else:
            logger.debug(
                "Broadcasting to %d clients (excluding sender). Data: %s",
                len(self.connected_clients) - 1,
                data,
            )

        for client_id, client_info in self.connected_clients.items():
            if include_sender or client_id != sender_id:
                try:
                    await client_info["websocket"].send_json(data)
                    logger.debug("Broadcasted to client %s", client_info["first_name"])
                except Exception as e:
                    logger.error(
                        "Error broadcasting to client %s: %s",
                        client_info["first_name"],
                        str(e),
                    )

    def _get_unique_first_name(self) -> str:
        """Get a unique first name for a new client."""
        used_names = set(
            client["first_name"] for client in self.connected_clients.values()
        )
        available_names = list(set(self.first_names) - used_names)
        if available_names:
            return random.choice(available_names)
        else:
            # If all names are taken, append a number to a random name
            base_name = random.choice(self.first_names)
            suffix = 1
            while f"{base_name}{suffix}" in used_names:
                suffix += 1
            return f"{base_name}{suffix}"


ws_manager = WebSocketManager()
