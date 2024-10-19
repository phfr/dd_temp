"""
Hello event handler for the DataDiVR-Backend.

This module defines the handler for the 'hello' event, demonstrating
a simple interaction between a client and the server.
"""

from utils.custom_logging import logger
from utils.websocket import ws_manager


@ws_manager.event("hello")
async def handle_hello(data: dict, websocket, client_info: dict):
    """
    Handle the hello event from clients.

    This function responds to a 'hello' event by sending a greeting back to the client.
    It demonstrates basic event handling and client interaction.

    Args:
        data (dict): The data sent with the hello event, expected to contain a 'name' field.
        websocket (WebSocket): The WebSocket connection object for the client.
        client_info (dict): Information about the client, not used in this handler.
    """
    name = data.get("name", "Guest")
    logger.info(f"Handling hello event for {name}")
    await websocket.send_json(
        {
            "event": "hello",
            "sender_name": "handle_hello_function",
            "message": f"Hello {name}!",
        }
    )
