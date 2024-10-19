from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import WebSocket

from utils.websocket_manager import WebSocketManager


@pytest.fixture
def ws_manager():
    return WebSocketManager()


@pytest.fixture
def mock_websocket():
    mock_websocket = Mock(spec=WebSocket)
    # Mock the required async methods for WebSocket
    mock_websocket.scope = {}
    mock_websocket.receive = AsyncMock()
    mock_websocket.send = AsyncMock()
    return mock_websocket


def test_add_client(ws_manager, mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    assert client_id in ws_manager.connected_clients
    assert ws_manager.connected_clients[client_id]["websocket"] == mock_websocket


def test_remove_client(ws_manager, mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    ws_manager.remove_client(client_id)
    assert client_id not in ws_manager.connected_clients


def test_get_client_info(ws_manager, mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    client_info = ws_manager.get_client_info(mock_websocket)
    assert client_info["client_id"] == client_id
    assert "first_name" in client_info


@pytest.mark.asyncio
async def test_event_decorator(ws_manager, mock_websocket):
    @ws_manager.event("test_event")
    async def test_handler(data, websocket, client_info):
        return data["message"]

    # client_id = ws_manager.add_client(mock_websocket)
    result = await ws_manager.handlers["test_event"](
        {"message": "Hello"}, mock_websocket
    )
    assert result == "Hello"


@pytest.mark.asyncio
async def test_handle_event(ws_manager, mock_websocket, mocker):
    # client_id = ws_manager.add_client(mock_websocket)

    # Register the event handler properly with the required parameters
    @ws_manager.event("test_event")
    async def test_handler(data, websocket, client_info):
        # Use websocket to send the message back
        await websocket.send_json({"message": data["message"]})
        return data["message"]

    # Patch the send_json method to check if it gets called
    mock_send = mocker.patch.object(mock_websocket, "send_json", new_callable=AsyncMock)

    # Call the handle_event function
    await ws_manager.handle_event("test_event", {"message": "Hello"}, mock_websocket)

    # Assert that send_json was called once with the correct message
    mock_send.assert_called_once_with({"message": "Hello"})
