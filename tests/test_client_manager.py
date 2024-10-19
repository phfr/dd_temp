import pytest
from fastapi import WebSocket

from utils.websocket.client_manager import ClientManager


@pytest.fixture
def client_manager():
    return ClientManager()


@pytest.fixture
def mock_websocket():
    # Create a mock WebSocket with dummy arguments
    return WebSocket(
        scope={"type": "websocket"}, receive=lambda: None, send=lambda _: None
    )


def test_add_client(client_manager, mock_websocket):
    client_id = client_manager.add_client(mock_websocket)
    assert client_id in client_manager.connected_clients
    assert client_manager.connected_clients[client_id].websocket == mock_websocket


def test_remove_client(client_manager, mock_websocket):
    client_id = client_manager.add_client(mock_websocket)
    client_manager.remove_client(client_id)
    assert client_id not in client_manager.connected_clients


def test_get_client_info(client_manager, mock_websocket):
    client_id = client_manager.add_client(mock_websocket)
    client_info = client_manager.get_client_info(mock_websocket)
    assert client_info["client_id"] == client_id
    assert "first_name" in client_info
