import typing
import fastapi
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: typing.Dict[int, fastapi.WebSocket] = {}

    async def connect(self, user_id:int,websocket:fastapi.WebSocket):
        await websocket.accept()
        self.active_connections[user_id]=websocket
        print(f"User {user_id} connected")
    def disconnect(self, user_id:int):
        self.active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected")
    
    async def send_to_user(self, user_id:int , message:str):
        ws=self.active_connections.get(user_id)
        if ws:
            await ws.send_text(message)

    async def broadcast(self, message:str):
        for ws in self.active_connections.values():
            await ws.send_text(message)
