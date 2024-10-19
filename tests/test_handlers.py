from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocket

from handlers.hello import handle_hello
from handlers.ping import handle_ping
from handlers.welcome import handle_welcome


@pytest.mark.asyncio
async def test_handle_welcome():
    mock_websocket = AsyncMock(spec=WebSocket)
    client_info = {"client_id": "test_id", "first_name": "Test"}
    await handle_welcome(client_info, mock_websocket)
    mock_websocket.send_json.assert_called_once()


@pytest.mark.asyncio
async def test_handle_hello():
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
    mock_websocket = AsyncMock(spec=WebSocket)
    await handle_ping(mock_websocket)
    mock_websocket.send_json.assert_called_once_with(
        {"event": "pong", "sender_name": "ping pong bot"}
    )
