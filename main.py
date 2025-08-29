from app.websocket.redis_pubsub import redis_subscriber
from app.accounts.views import router as account_router
from app.websocket.routes import router as ws_router
from fastapi.middleware.cors import CORSMiddleware
from app.home.views import router as home_router
from contextlib import asynccontextmanager
from database import init_db
from app.accounts.models import User
from fastapi import FastAPI
import asyncio

redis_subscriber_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_subscriber_task
    redis_subscriber_task = asyncio.create_task(redis_subscriber())
    yield
    if redis_subscriber_task:
        redis_subscriber_task.cancel()
        try:
            await redis_subscriber_task 
        except asyncio.CancelledError:
            pass

app = FastAPI(title="FastAPI + Tortoise + PostgreSQL",lifespan=lifespan)

init_db(app)

app.include_router(home_router)
app.include_router(account_router)
app.include_router(ws_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI with Tortoise ORM & PostgreSQL"}

@app.get("/users")
async def read_root():
    users = await User.all()[:0]
    return users



# fastapi dev main.py --host 192.168.1.111 --port 4500