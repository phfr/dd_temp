"""
Welcome event handler for the DataDiVR-Backend.

This module defines the handler for the 'welcome' event, which is triggered
when a new client connects to the WebSocket server.
"""

from utils.websocket import ws_manager


@ws_manager.event("welcome")
async def handle_welcome(client_info, websocket):
    """
    Handle the welcome event for new clients.

    This function is called automatically when a new client connects to the
    WebSocket server. It sends a personalized welcome message to the client.

    Args:
        client_info (dict): A dictionary containing information about the client,
                            including 'client_id' and 'first_name'.
        websocket (WebSocket): The WebSocket connection object for the client.
    """
    client_id = client_info["client_id"]
    client_name = client_info["first_name"]

    welcome_message = f"habedere! we will call you {client_name}! ({client_id})"

    await websocket.send_json(
        {
            "event": "welcome",
            "sender_name": "handle_welcome()",
            "message": welcome_message,
        }
    )
