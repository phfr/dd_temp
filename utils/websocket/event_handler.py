import time
from typing import Any, Callable, Dict

from fastapi import WebSocket

from utils.custom_logging import logger


class EventHandler:
    def __init__(
        self,
        handlers: Dict[str, Callable],
        get_client_info: Callable,
        broadcast: Callable,
    ):
        self.handlers = handlers
        self.get_client_info = get_client_info
        self.broadcast_func = broadcast

    async def handle_event(
        self, event_name: str, data: Dict[Any, Any], websocket: WebSocket
    ):
        client_info = self.get_client_info(websocket)
        client_id, client_name = client_info["client_id"], client_info["first_name"]

        logger.debug(
            "Received event: %s with data: %s from client %s (%s)",
            event_name,
            data,
            client_id,
            client_name,
        )

        # if we have an event handler for this event, execute it
        # otherwise, broadcast the event to all clients except the sender
        if event_name in self.handlers:
            start_time = time.time()
            await self.handlers[event_name](data, websocket)
            duration = time.time() - start_time
            logger.debug(
                "Event handler '%s' took %.5f seconds to execute", event_name, duration
            )
        else:
            logger.debug(
                "Unknown event received: %s from client %s. Broadcasting to all clients except sender.",
                event_name,
                client_name,
            )
            await self.broadcast_func(
                {
                    "event": event_name,
                    "sender_id": client_id,
                    "sender_name": client_name,
                    "data": data,
                }
            )
