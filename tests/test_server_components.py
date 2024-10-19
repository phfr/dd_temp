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
    return create_fastapi_app()


def test_create_fastapi_app(app):
    assert app is not None


@pytest.mark.asyncio
async def test_add_static_files(app):
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
    load_event_handlers()
    assert "welcome" in ws_manager.handlers
    assert "hello" in ws_manager.handlers
    assert "ping" in ws_manager.handlers


@pytest.mark.asyncio
async def test_load_route_handlers(app):
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
