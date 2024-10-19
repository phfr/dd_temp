import uuid
from typing import Any, Dict

from fastapi import WebSocket

from utils.custom_logging import logger
from utils.names import name_manager

from .client_info import ClientInfo


class ClientManager:
    def __init__(self):
        self.connected_clients: Dict[str, ClientInfo] = {}
        self._client_lookup: Dict[WebSocket, str] = {}

    def get_client_info(self, websocket: WebSocket) -> Dict[str, Any]:
        client_id = self._client_lookup.get(websocket)
        if client_id:
            client_info = self.connected_clients[client_id]
            return {"client_id": client_id, "first_name": client_info.first_name}
        return {"client_id": None, "first_name": None}

    def add_client(self, client: WebSocket) -> str:
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

    def get_all_clients(self):
        return list(self.connected_clients.values())
