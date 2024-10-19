"""
WebSocket management module for the DataDiVR-Backend.

This module provides a WebSocketManager class that integrates various components
to manage WebSocket connections, events, and client information in the DataDiVR-Backend system.
"""

from typing import Callable, Dict

from .broadcaster import Broadcaster
from .client_manager import ClientManager
from .event_decorator import event_decorator
from .event_handler import EventHandler


class WebSocketManager:
    """
    Manages WebSocket connections, events, and client information for the DataDiVR-Backend.

    This class integrates ClientManager, Broadcaster, and EventHandler to provide
    a comprehensive WebSocket management solution.
    """

    def __init__(self):
        """
        Initialize the WebSocketManager with its component managers and handlers.
        """
        self.handlers: Dict[str, Callable] = {}
        self.client_manager = ClientManager()
        self.broadcaster = Broadcaster(self.client_manager.get_client_info)
        self.event_handler = EventHandler(
            self.handlers, self.client_manager.get_client_info, self.broadcast
        )
        self.event = event_decorator(self.handlers, self.client_manager.get_client_info)

    def get_client_info(self, websocket):
        """
        Get information about a client connected via WebSocket.

        Args:
            websocket: The WebSocket connection of the client.

        Returns:
            dict: A dictionary containing client information.
        """
        return self.client_manager.get_client_info(websocket)

    def add_client(self, client):
        """
        Add a new client to the WebSocket manager.

        Args:
            client: The WebSocket connection of the new client.

        Returns:
            str: The unique ID assigned to the new client.
        """
        return self.client_manager.add_client(client)

    def remove_client(self, client_id):
        """
        Remove a client from the WebSocket manager.

        Args:
            client_id (str): The unique ID of the client to remove.
        """
        self.client_manager.remove_client(client_id)

    async def handle_event(self, event_name, data, websocket):
        """
        Handle an incoming WebSocket event.

        Args:
            event_name (str): The name of the event to handle.
            data (dict): The data associated with the event.
            websocket: The WebSocket connection that received the event.
        """
        await self.event_handler.handle_event(event_name, data, websocket)

    async def broadcast(self, data, include_sender=False):
        """
        Broadcast data to all connected clients.

        Args:
            data (dict): The data to broadcast.
            include_sender (bool, optional): Whether to include the sender in the broadcast. Defaults to False.
        """
        clients = self.client_manager.get_all_clients()
        await self.broadcaster.broadcast(data, clients, include_sender)


# Create a global instance of WebSocketManager
ws_manager = WebSocketManager()
