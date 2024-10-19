from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import WebSocket

from utils.websocket import ws_manager
from utils.websocket.event_handler import EventHandler


@pytest.fixture
def mock_handlers():
    return {"test_event": lambda data, websocket: None}


@pytest.fixture
def mock_get_client_info():
    return lambda websocket: {"client_id": "test_id", "first_name": "Test"}


@pytest.fixture
def mock_broadcast():
    return lambda data, include_sender=False: None


@pytest.fixture
def event_handler(mock_handlers, mock_get_client_info, mock_broadcast):
    return EventHandler(mock_handlers, mock_get_client_info, mock_broadcast)


@pytest.fixture
def mock_websocket():
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
async def test_handle_event(mock_websocket, mocker):
    mock_handler = AsyncMock()
    ws_manager.handlers["test_event"] = mock_handler

    await ws_manager.event_handler.handle_event(
        "test_event", {"data": "test"}, mock_websocket
    )

    mock_handler.assert_called_once_with({"data": "test"}, mock_websocket)


@pytest.mark.asyncio
async def test_broadcast(event_handler, mock_websocket, mocker):
    mock_broadcast = AsyncMock()
    event_handler.broadcast_func = mock_broadcast

    await event_handler.handle_event("unknown_event", {"data": "test"}, mock_websocket)

    mock_broadcast.assert_called_once_with(
        {
            "event": "unknown_event",
            "sender_id": "test_id",
            "sender_name": "Test",
            "data": {"data": "test"},
        }
    )
