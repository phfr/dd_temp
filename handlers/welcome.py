from utils.websocket import ws_manager


@ws_manager.event("welcome")
async def handle_welcome(client_info, websocket):
    """Handle the welcome event for new clients."""
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
