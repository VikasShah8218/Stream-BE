# app/websocket/manager.py
from fastapi import WebSocket
from typing import List,Dict
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket,user_id: int):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        for user, sockets in self.active_connections.items():
            if websocket in sockets:
                sockets.remove(websocket)
                if not sockets:
                    del self.active_connections[user]
                break

    async def send_to_user(self, user_id: str, message: str):
        sockets = self.active_connections.get(user_id, [])
        for connection in sockets:
            await connection.send_text(message)

    async def broadcast(self, message: str):
        print("==============================> ", "Broadcast Message")
        for sockets in self.active_connections.values():
            for connection in sockets:
                await connection.send_text(message)

    def list_active_users(self) -> List[str]:
        return list(self.active_connections.keys())


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         if websocket in self.active_connections:
#             self.active_connections.remove(websocket)

#     async def send_to_all(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

#     def list_active_connections(self) -> int:
#         return len(self.active_connections)

# manager = ConnectionManager()
manager = ConnectionManager()
