from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class ClientInfo:
    websocket: WebSocket
    client_id: str
    first_name: str
