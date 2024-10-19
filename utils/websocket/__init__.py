"""
WebSocket utilities initialization for the DataDiVR-Backend.

This module imports and exposes the WebSocketManager instance for use
throughout the application.
"""

from .websocket_manager import ws_manager

# Specify which symbols should be accessible when using "from utils.websocket import *"
__all__ = ["ws_manager"]
