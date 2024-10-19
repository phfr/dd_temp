"""
Main application module for the DataDiVR-Backend WebSocket server.

This module sets up the DataDiVR-Backend application, configures static file serving,
loads event handlers and route handlers, and sets up the WebSocket endpoint.
"""

from dotenv import load_dotenv

from server_components import (
    add_custom_static_folder,
    add_static_files,
    add_websocket_endpoint,
    create_fastapi_app,
    load_event_handlers,
    load_route_handlers,
)

# Load environment variables from .env file
load_dotenv()


def create_app():
    """
    Create and configure the DataDiVR-Backend application.

    This function sets up the DataDiVR-Backend app, adds static file serving,
    loads event handlers and route handlers, and sets up the WebSocket endpoint.

    Returns:
        FastAPI: The configured DataDiVR-Backend application.
    """
    app = create_fastapi_app()

    add_static_files(app)  # serve files in static
    add_custom_static_folder(
        app, "static_project", "project_files/static/"
    )  # custom static folder

    load_event_handlers()  # websocket event handlers in handlers/
    load_route_handlers(app)  # api routes in routes/

    # TODO: load custom route_handlers(app, '/project_files/routes/')
    # TODO: load_custom_event_handlers(app, '/project_files/handlers/')

    add_websocket_endpoint(app)  # websocket server
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
