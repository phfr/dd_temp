"""
Client information module for WebSocket connections in the DataDiVR-Backend.

This module defines the ClientInfo class, which represents the information
associated with a connected WebSocket client in the DataDiVR-Backend system.
"""

from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class ClientInfo:
    """
    Represents information about a connected WebSocket client.

    This dataclass stores essential information about a client connected
    to the DataDiVR-Backend via WebSocket, including the WebSocket connection,
    client ID, and the client's assigned name.

    Attributes:
        websocket (WebSocket): The WebSocket connection object for the client.
        client_id (str): A unique identifier for the client.
        first_name (str): The assigned name for the client.
    """

    websocket: WebSocket
    client_id: str
    first_name: str
