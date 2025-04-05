from app.websocket.manager import manager
import redis.asyncio as aioredis
import asyncio


REDIS_URL = "redis://127.0.0.1:6379"

async def redis_subscriber():
    redis = await aioredis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe("broadcast")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await manager.broadcast(message["data"].decode())
    except asyncio.CancelledError:
        await pubsub.unsubscribe("broadcast")
        await pubsub.close()
        await redis.close()

# from app.websocket.manager import manager
# import redis.asyncio as aioredis
# import asyncio
# import json

# REDIS_URL = "redis://127.0.0.1:6379"

# async def redis_subscriber():
#     redis = await aioredis.from_url(REDIS_URL)
#     pubsub = redis.pubsub()
#     await pubsub.subscribe("broadcast")

#     try:
#         async for message in pubsub.listen():
#             if message["type"] == "message":
#                 # When a broadcast message is received, send to all local connections
#                 # Note: This only sends to connections on this worker
#                 # For true multi-worker broadcasting, you'd need a different approach
#                 await manager.broadcast_local(message["data"].decode())
#     except asyncio.CancelledError:
#         await pubsub.unsubscribe("broadcast")
#         await pubsub.close()
#         await redis.close()