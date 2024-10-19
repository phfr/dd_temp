from typing import Callable, Dict

from .broadcaster import Broadcaster
from .client_manager import ClientManager
from .event_decorator import event_decorator
from .event_handler import EventHandler


class WebSocketManager:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.client_manager = ClientManager()
        self.broadcaster = Broadcaster(self.client_manager.get_client_info)
        self.event_handler = EventHandler(
            self.handlers, self.client_manager.get_client_info, self.broadcast
        )
        self.event = event_decorator(self.handlers, self.client_manager.get_client_info)

    def get_client_info(self, websocket):
        return self.client_manager.get_client_info(websocket)

    def add_client(self, client):
        return self.client_manager.add_client(client)

    def remove_client(self, client_id):
        self.client_manager.remove_client(client_id)

    async def handle_event(self, event_name, data, websocket):
        await self.event_handler.handle_event(event_name, data, websocket)

    async def broadcast(self, data, include_sender=False):
        clients = self.client_manager.get_all_clients()
        await self.broadcaster.broadcast(data, clients, include_sender)


ws_manager = WebSocketManager()
