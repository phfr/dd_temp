"""
Unit tests for the EventHandler class in the DataDiVR-Backend.

This module contains pytest fixtures and test cases to verify the functionality
of the EventHandler class, which manages WebSocket event handling.
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import WebSocket

from utils.websocket import ws_manager
from utils.websocket.event_handler import EventHandler


@pytest.fixture
def mock_handlers():
    """
    Fixture to create mock event handlers.

    Returns:
        dict: A dictionary with a mock event handler.
    """
    return {"test_event": lambda data, websocket: None}


@pytest.fixture
def mock_get_client_info():
    """
    Fixture to create a mock function for getting client info.

    Returns:
        function: A mock function that returns dummy client info.
    """
    return lambda websocket: {"client_id": "test_id", "first_name": "Test"}


@pytest.fixture
def mock_broadcast():
    """
    Fixture to create a mock broadcast function.

    Returns:
        function: A mock function for broadcasting messages.
    """
    return lambda data, include_sender=False: None


@pytest.fixture
def event_handler(mock_handlers, mock_get_client_info, mock_broadcast):
    """
    Fixture to create an EventHandler instance with mock dependencies.

    Returns:
        EventHandler: An instance of EventHandler with mock handlers and functions.
    """
    return EventHandler(mock_handlers, mock_get_client_info, mock_broadcast)


@pytest.fixture
def mock_websocket():
    """
    Fixture to create a mock WebSocket object.

    Returns:
        Mock: A mock WebSocket instance.
    """
    return Mock(spec=WebSocket)


@pytest.mark.asyncio
async def test_handle_event(mock_websocket, mocker):
    """
    Test the handle_event method of EventHandler for a known event.

    Verifies that the correct handler is called when a known event is received.
    """
    mock_handler = AsyncMock()
    ws_manager.handlers["test_event"] = mock_handler

    await ws_manager.event_handler.handle_event(
        "test_event", {"data": "test"}, mock_websocket
    )

    mock_handler.assert_called_once_with({"data": "test"}, mock_websocket)


@pytest.mark.asyncio
async def test_broadcast(event_handler, mock_websocket, mocker):
    """
    Test the handle_event method of EventHandler for an unknown event.

    Verifies that unknown events are broadcast to all clients.
    """
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
