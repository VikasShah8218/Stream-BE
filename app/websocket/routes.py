from fastapi import APIRouter, WebSocket, WebSocketDisconnect , Query
from app.websocket.manager import manager
import logging
from app.websocket.ws_auth import websocket_authenticate_user
import redis.asyncio as aioredis

logger = logging.getLogger("Stream")

router = APIRouter()
# REDIS_URL = "redis://localhost:6379"
REDIS_URL = "redis://localhost"

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user = await websocket_authenticate_user(websocket)
    await manager.connect(websocket, user_id = user.id)
    # await manager.connect(websocket)
    redis = await aioredis.from_url(REDIS_URL)
    connection_open = True
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"[{user.username}] sent: {data}")
            await broadcast_ws_message(data)
            print(f"[{user.username}] sent: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        connection_open = False
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if connection_open:
            try:
                logger.info(f"Closing WebSocket connection")
                await websocket.close()
            except Exception as e:
                logger.info(f"Error during WebSocket close: {e}")
        logger.info(f"WebSocket connection cleanup done.")


async def broadcast_ws_message(message: str):
    # users = manager.list_active_users()
    # message = f"Online Users: {', '.join(users)}"
    redis = await aioredis.from_url(REDIS_URL)
    await redis.publish("broadcast", message)
    await redis.close()