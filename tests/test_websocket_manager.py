from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import WebSocket

from utils.websocket import ws_manager


@pytest.fixture
def mock_websocket():
    mock_websocket = Mock(spec=WebSocket)
    mock_websocket.scope = {}
    mock_websocket.receive = AsyncMock()
    mock_websocket.send = AsyncMock()
    return mock_websocket


def test_add_client(mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    assert client_id in ws_manager.client_manager.connected_clients
    assert (
        ws_manager.client_manager.connected_clients[client_id].websocket
        == mock_websocket
    )


def test_remove_client(mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    ws_manager.remove_client(client_id)
    assert client_id not in ws_manager.client_manager.connected_clients


def test_get_client_info(mock_websocket):
    client_id = ws_manager.add_client(mock_websocket)
    client_info = ws_manager.get_client_info(mock_websocket)
    assert client_info["client_id"] == client_id
    assert "first_name" in client_info


@pytest.mark.asyncio
async def test_event_decorator(mock_websocket):
    @ws_manager.event("test_event")
    async def test_handler(data, websocket, client_info):
        return data["message"]

    result = await ws_manager.handlers["test_event"](
        {"message": "Hello"}, mock_websocket
    )
    assert result == "Hello"


@pytest.mark.asyncio
async def test_handle_event(mock_websocket, mocker):
    @ws_manager.event("test_event")
    async def test_handler(data, websocket, client_info):
        await websocket.send_json({"message": data["message"]})
        return data["message"]

    mock_send = mocker.patch.object(mock_websocket, "send_json", new_callable=AsyncMock)

    await ws_manager.handle_event("test_event", {"message": "Hello"}, mock_websocket)

    mock_send.assert_called_once_with({"message": "Hello"})


@pytest.mark.asyncio
async def test_broadcast(mock_websocket, mocker):
    mock_send = mocker.patch.object(mock_websocket, "send_json", new_callable=AsyncMock)

    ws_manager.add_client(mock_websocket)
    await ws_manager.broadcast({"message": "Broadcast test"})

    mock_send.assert_called_once_with({"message": "Broadcast test"})
