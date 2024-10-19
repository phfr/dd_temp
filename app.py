"""Spin up websocket, api, and static file server."""

from server_components import (
    add_custom_static_folder,
    add_static_files,
    add_websocket_endpoint,
    create_fastapi_app,
    load_event_handlers,
    load_route_handlers,
)


def create_app():
    """choose what components we want to run and do so."""

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
