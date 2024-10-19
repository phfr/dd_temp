class Broadcaster:
    def __init__(self, get_client_info):
        self.get_client_info = get_client_info

    async def broadcast(self, data, clients, include_sender=False):
        sender_id = data.get("sender_id")
        for client in clients:
            if include_sender or client.client_id != sender_id:
                await self.send_message(client.websocket, data)

    async def send_message(self, websocket, data):
        await websocket.send_json(data)
