from utils.websocket_manager import ws_manager


@ws_manager.event("hello")
async def handle_hello(data: dict, websocket, client_info: dict):
    name = data.get("name", "Guest")
    await websocket.send_json(
        {
            "event": "hello",
            "sender_name": "handle_hello_function",
            "message": f"Hello {name}!",
        }
    )
