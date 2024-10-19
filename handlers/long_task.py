"""
Long task event handler for the DataDiVR-Backend.

This module defines the handler for the 'long_task' event, demonstrating
how to handle asynchronous long-running tasks and broadcast results.
"""

import asyncio

from utils.websocket import ws_manager


@ws_manager.event("long_task")
async def handle_long_task():
    """
    Handle a long-running task and broadcast the result.

    This function simulates a long-running task using asyncio.sleep,
    then broadcasts a completion message to all connected clients.
    It demonstrates handling of asynchronous operations and server-initiated broadcasts.
    """
    await asyncio.sleep(5)  # Simulate a long-running task
    message = {
        "event": "long_task_completed",
        "sender_name": "long_task_batch_processing_system",
        "data": {"result": "yolo!"},
    }
    # Broadcast completion message to all clients
    await ws_manager.broadcast(message)
