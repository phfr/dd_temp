"""
Client management module for WebSocket connections in the DataDiVR-Backend.

This module provides a ClientManager class to handle client connections,
including adding, removing, and retrieving client information.
"""

import uuid
from typing import Any, Dict, List

from fastapi import WebSocket

from ..custom_logging import logger
from ..names import name_manager
from .client_info import ClientInfo


class ClientManager:
    """
    Manages WebSocket client connections for the DataDiVR-Backend.

    This class keeps track of connected clients, their WebSocket connections,
    and associated information such as client IDs and names.
    """

    def __init__(self):
        """
        Initialize the ClientManager with empty dictionaries for client tracking.
        """
        self.connected_clients: Dict[str, ClientInfo] = {}
        self._client_lookup: Dict[WebSocket, str] = {}

    def get_client_info(self, websocket: WebSocket) -> Dict[str, Any]:
        """
        Retrieve client information for a given WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket connection to look up.

        Returns:
            Dict[str, Any]: A dictionary containing client_id and first_name,
                            or None values if the client is not found.
        """
        client_id = self._client_lookup.get(websocket)
        if client_id:
            client_info = self.connected_clients[client_id]
            return {"client_id": client_id, "first_name": client_info.first_name}
        return {"client_id": None, "first_name": None}

    def add_client(self, client: WebSocket) -> str:
        """
        Add a new client to the manager and assign a unique name.

        Args:
            client (WebSocket): The WebSocket connection of the new client.

        Returns:
            str: The unique client ID assigned to the new client.
        """
        client_id = str(uuid.uuid4())
        used_names = {
            client_info.first_name for client_info in self.connected_clients.values()
        }
        first_name = name_manager.get_unique_name(used_names)
        self.connected_clients[client_id] = ClientInfo(
            websocket=client, client_id=client_id, first_name=first_name
        )
        self._client_lookup[client] = client_id
        logger.info("New client connected. ID: %s, Name: %s", client_id, first_name)
        logger.debug("Total connected clients: %d", len(self.connected_clients))
        return client_id

    def remove_client(self, client_id: str):
        """
        Remove a client from the manager.

        Args:
            client_id (str): The unique ID of the client to remove.
        """
        if client_id in self.connected_clients:
            client_info = self.connected_clients[client_id]
            del self.connected_clients[client_id]
            del self._client_lookup[client_info.websocket]
            logger.info(
                "Client disconnected. ID: %s, Name: %s",
                client_id,
                client_info.first_name,
            )
            logger.debug("Total connected clients: %d", len(self.connected_clients))
        else:
            logger.warning("Attempted to remove non-existent client. ID: %s", client_id)

    def get_all_clients(self) -> List[ClientInfo]:
        """
        Retrieve a list of all connected clients.

        Returns:
            List[ClientInfo]: A list of ClientInfo objects representing all connected clients.
        """
        return list(self.connected_clients.values())
