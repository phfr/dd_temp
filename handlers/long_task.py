"""
Long task event handler for the DataDiVR-Backend.

This module defines the handler for the 'long_task' event, demonstrating
how to handle asynchronous long-running tasks and broadcast results using background tasks.
"""

import asyncio

from utils.API_framework import BackgroundTasks
from utils.websocket import ws_manager


@ws_manager.event("long_task")
async def handle_long_task(background_tasks: BackgroundTasks):
    """
    Handle a long-running task using background tasks and broadcast the result.

    This function initiates a long-running task as a background task,
    allowing the WebSocket connection to remain responsive.
    """
    background_tasks.add_task(run_long_task)
    return {"message": "Long task initiated"}


async def run_long_task():
    """
    Perform the long-running task and broadcast the result.

    This function simulates a long-running task using asyncio.sleep,
    then broadcasts a completion message to all connected clients.
    """
    await asyncio.sleep(5)  # Simulate a long-running task
    message = {
        "event": "long_task_completed",
        "sender_name": "long_task_batch_processing_system",
        "data": {"result": "yolo!"},
    }
    # Broadcast completion message to all clients
    await ws_manager.broadcast(message)
