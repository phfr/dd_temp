"""
Integration tests for server components of the DataDiVR-Backend.

This module contains pytest fixtures and test cases to verify the functionality
of various server components, including static file serving, event handlers,
route handlers, and WebSocket endpoints.
"""

import os
import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
from httpx import ASGITransport, AsyncClient

from server_components import (
    add_static_files,
    create_fastapi_app,
    load_event_handlers,
    load_route_handlers,
    websocket_endpoint,
)
from utils.websocket import ws_manager


@pytest.fixture
def app():
    """
    Fixture to create a FastAPI app instance for testing.

    Returns:
        FastAPI: A new instance of the FastAPI application.
    """
    return create_fastapi_app()


def test_create_fastapi_app(app):
    """
    Test the creation of the FastAPI app.

    Verifies that the create_fastapi_app function returns a valid FastAPI instance.
    """
    assert app is not None


@pytest.mark.asyncio
async def test_add_static_files(app):
    """
    Test the addition of static files to the FastAPI app.

    Verifies that static files are correctly served after being added to the app.
    """
    # Use the existing static directory
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    os.makedirs(static_dir, exist_ok=True)

    # Create a unique filename for our test
    test_filename = f"test_{uuid.uuid4().hex}.txt"
    test_file_path = os.path.join(static_dir, test_filename)

    try:
        # Create a test file
        with open(test_file_path, "w") as f:
            f.write("Test content")

        # Add static files to the app
        add_static_files(app)

        # Test the route using AsyncClient with explicit ASGITransport
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.get(f"/static/{test_filename}")

        assert response.status_code == 200
        assert response.text == "Test content"

    finally:
        # Clean up the test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def test_load_event_handlers():
    """
    Test the loading of event handlers.

    Verifies that event handlers are correctly loaded and registered.
    """
    load_event_handlers()
    assert "welcome" in ws_manager.handlers
    assert "hello" in ws_manager.handlers
    assert "ping" in ws_manager.handlers


@pytest.mark.asyncio
async def test_load_route_handlers(app):
    """
    Test the loading of route handlers.

    Verifies that route handlers are correctly loaded and registered with the app.
    """
    load_route_handlers(app)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_websocket_endpoint():
    mock_websocket = AsyncMock(spec=WebSocket)
    mock_websocket.receive_json.side_effect = [
        {"event": "hello", "name": "John"},
        WebSocketDisconnect(),
    ]

    await websocket_endpoint(mock_websocket)

    mock_websocket.accept.assert_called_once()
    assert len(ws_manager.client_manager.connected_clients) == 0
