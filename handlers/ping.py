"""Handles ping events for the websocket connection."""

from utils.websocket import ws_manager


@ws_manager.event("ping")
async def handle_ping(websocket):
    """Handle ping event by responding with a pong."""
    await websocket.send_json({"event": "pong", "sender_name": "ping pong bot"})
