"""
Server components module for the DataDiVR-Backend.

This module contains functions for creating and configuring the DataDiVR-Backend,
including static file serving, event handlers, route handlers, and WebSocket endpoints.
"""

import importlib
import json
import os
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from websockets.exceptions import ConnectionClosedOK

from utils.custom_logging import logger
from utils.websocket import ws_manager


def create_fastapi_app():
    """
    Create a new FastAPI instance for the DataDiVR-Backend.

    Returns:
        FastAPI: A new FastAPI instance for the DataDiVR-Backend.
    """
    app = FastAPI()
    return app


def add_static_files(app):
    """
    Add static file serving to the DataDiVR-Backend.

    Args:
        app (FastAPI): The DataDiVR-Backend FastAPI instance.
    """
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.debug("added static files route at %s", "/static")


def load_event_handlers():
    """
    Load event handlers from the 'handlers' directory for the DataDiVR-Backend.

    This function dynamically imports all Python modules in the 'handlers' directory,
    excluding '__init__.py'.
    """
    for filename in os.listdir("handlers"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"handlers.{filename[:-3]}"
            importlib.import_module(module_name)
            logger.debug("Loaded handlers from %s", module_name)


def load_route_handlers(app):
    """
    Load route handlers from the 'routes' directory and add them to the DataDiVR-Backend.

    Args:
        app (FastAPI): The DataDiVR-Backend FastAPI instance.
    """
    for filename in os.listdir("routes"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"routes.{filename[:-3]}"
            module = importlib.import_module(module_name)
            app.include_router(module.route)
            logger.debug("Added routes from module: %s", module_name)


async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections and events for the DataDiVR-Backend.

    This function manages the lifecycle of a WebSocket connection, including
    accepting the connection, handling events, and cleaning up on disconnect.

    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()
    client_id = ws_manager.add_client(websocket)

    try:
        # when user connects, send them the welcome event
        # this is like a init() call
        await ws_manager.handle_event("welcome", {}, websocket)

        while True:
            data = await websocket.receive_json()
            event_name = data.get("event")
            await ws_manager.handle_event(event_name, data, websocket)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for client {client_id}")
    except (ConnectionClosedOK, json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error for client {client_id}: {e}")
    finally:
        ws_manager.remove_client(client_id)
        logger.info(f"Removed client {client_id}")


def add_websocket_endpoint(app):
    """
    Add the WebSocket endpoint to the DataDiVR-Backend.

    Args:
        app (FastAPI): The DataDiVR-Backend FastAPI instance.
    """
    app.add_api_websocket_route("/ws", websocket_endpoint)


def add_custom_static_folder(
    app, route: str, directory: str, name: Optional[str] = None
):
    """
    Add a custom static folder to the DataDiVR-Backend.

    Args:
        app (FastAPI): The DataDiVR-Backend FastAPI instance.
        route (str): The URL path where the static files will be served.
        directory (str): The directory path containing the static files.
        name (Optional[str], optional): A name for this mount point. Defaults to None.
    """
    if not route.startswith("/"):
        route = f"/{route}"

    app.mount(
        route, StaticFiles(directory=directory), name=name or f"static_{directory}"
    )
    logger.debug("Added custom static folder: %s at route %s", directory, route)
