"""
Unit tests for WebSocket event handlers in the DataDiVR-Backend.

This module contains pytest fixtures and test cases to verify the functionality
of various WebSocket event handlers, including welcome, hello, and ping handlers.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocket

from handlers.hello import handle_hello
from handlers.ping import handle_ping
from handlers.welcome import handle_welcome


@pytest.mark.asyncio
async def test_handle_welcome():
    """
    Test the welcome event handler.

    Verifies that the welcome handler sends the correct JSON response
    when a new client connects.
    """
    mock_websocket = AsyncMock(spec=WebSocket)
    client_info = {"client_id": "test_id", "first_name": "Test"}
    await handle_welcome(client_info, mock_websocket)
    mock_websocket.send_json.assert_called_once()


@pytest.mark.asyncio
async def test_handle_hello():
    """
    Test the hello event handler.

    Verifies that the hello handler sends the correct JSON response
    with a personalized greeting when receiving a hello event.
    """
    mock_websocket = AsyncMock(spec=WebSocket)
    data = {"name": "John"}
    client_info = {"client_id": "test_id", "first_name": "Test"}
    await handle_hello(data, mock_websocket, client_info)
    mock_websocket.send_json.assert_called_once_with(
        {
            "event": "hello",
            "sender_name": "handle_hello_function",
            "message": "Hello John!",
        }
    )


@pytest.mark.asyncio
async def test_handle_ping():
    """
    Test the ping event handler.

    Verifies that the ping handler sends the correct JSON response
    with a 'pong' message when receiving a ping event.
    """
    mock_websocket = AsyncMock(spec=WebSocket)
    await handle_ping(mock_websocket)
    mock_websocket.send_json.assert_called_once_with(
        {"event": "pong", "sender_name": "ping pong bot"}
    )
