"""
Unit tests for the ClientManager class in the DataDiVR-Backend.

This module contains pytest fixtures and test cases to verify the functionality
of the ClientManager class, which manages WebSocket client connections.
"""

import pytest
from fastapi import WebSocket

from utils.websocket.client_manager import ClientManager


@pytest.fixture
def client_manager():
    """
    Fixture to create a fresh ClientManager instance for each test.

    Returns:
        ClientManager: A new instance of the ClientManager class.
    """
    return ClientManager()


@pytest.fixture
def mock_websocket():
    """
    Fixture to create a mock WebSocket object for testing.

    Returns:
        WebSocket: A mock WebSocket instance with dummy arguments.
    """
    return WebSocket(
        scope={"type": "websocket"}, receive=lambda: None, send=lambda _: None
    )


def test_add_client(client_manager, mock_websocket):
    """
    Test adding a new client to the ClientManager.

    Verifies that a new client is correctly added and assigned a unique ID.
    """
    client_id = client_manager.add_client(mock_websocket)
    assert client_id in client_manager.connected_clients
    assert client_manager.connected_clients[client_id].websocket == mock_websocket


def test_remove_client(client_manager, mock_websocket):
    """
    Test removing a client from the ClientManager.

    Verifies that a client can be successfully removed after being added.
    """
    client_id = client_manager.add_client(mock_websocket)
    client_manager.remove_client(client_id)
    assert client_id not in client_manager.connected_clients


def test_get_client_info(client_manager, mock_websocket):
    """
    Test retrieving client information from the ClientManager.

    Verifies that correct client information can be retrieved for a connected client.
    """
    client_id = client_manager.add_client(mock_websocket)
    client_info = client_manager.get_client_info(mock_websocket)
    assert client_info["client_id"] == client_id
    assert "first_name" in client_info
