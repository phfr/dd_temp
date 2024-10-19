"""
Broadcaster module for WebSocket communication in the DataDiVR-Backend.

This module provides a Broadcaster class for sending messages to multiple
WebSocket clients in the DataDiVR-Backend system.
"""

from typing import Any, Callable, Dict, List

from websockets.exceptions import ConnectionClosed

from ..custom_logging import logger


class Broadcaster:
    """
    Manages broadcasting of messages to multiple WebSocket clients.

    This class provides functionality to send messages to all connected clients
    or a subset of clients, with options to exclude specific clients.
    """

    def __init__(self, get_client_info: Callable):
        """
        Initialize the Broadcaster with a function to get client information.

        Args:
            get_client_info (Callable): A function that returns client information given a WebSocket.
        """
        self.get_client_info = get_client_info

    async def broadcast(
        self,
        data: Dict[Any, Any],
        clients: List[Any],
        include_sender: bool = False,
    ):
        """
        Broadcast a message to multiple clients.

        This method sends the provided data to all specified clients, with an option
        to exclude the sender of the message.

        Args:
            data (Dict[Any, Any]): The message data to be broadcast.
            clients (List[Any]): A list of client objects to broadcast to.
            include_sender (bool, optional): Whether to include the sender in the broadcast. Defaults to False.

        Returns:
            int: The number of clients the message was successfully sent to.
        """
        sender_id = data.get("sender_id")
        successful_broadcasts = 0

        for client in clients:
            client_id = self.get_client_info(client.websocket)["client_id"]
            if client_id != sender_id or include_sender:
                try:
                    await client.websocket.send_json(data)
                    successful_broadcasts += 1
                except ConnectionClosed:
                    logger.warning(
                        f"Failed to send message to client {client_id}: Connection closed"
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending message to client {client_id}: {str(e)}"
                    )

        logger.debug(f"Broadcast message to {successful_broadcasts} clients")
        return successful_broadcasts

    async def send_message(self, websocket, data):
        await websocket.send_json(data)
