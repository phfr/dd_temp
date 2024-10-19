"""
Ping event handler for the DataDiVR-Backend.

This module defines the handler for the 'ping' event, which responds
to client ping requests with a 'pong' message.
"""

from utils.websocket import ws_manager


@ws_manager.event("ping")
async def handle_ping(websocket):
    """
    Handle ping events from clients.

    This function responds to a 'ping' event by sending a 'pong' message
    back to the client, demonstrating a simple request-response pattern.

    Args:
        websocket (WebSocket): The WebSocket connection object for the client.
    """
    await websocket.send_json({"event": "pong", "sender_name": "ping pong bot"})
