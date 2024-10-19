"""Example of running a long async and then emitting a new broadcast event."""

import asyncio

from utils.websocket import ws_manager


@ws_manager.event("long_task")
async def handle_long_task():
    """Handle a long-running task and broadcast the result."""
    await asyncio.sleep(5)  # Simulate a long-running task
    message = {
        "event": "long_task_completed",
        "sender_name": "long_task_batch_processing_system",
        "data": {"result": "yolo!"},
    }
    # long task is complete, lets emit a new event to all clients
    await ws_manager.broadcast(message)
