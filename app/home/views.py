from app.accounts.auth import get_current_user
from app.websocket.manager import manager
from app.accounts.models import User
import redis.asyncio as aioredis
from fastapi import APIRouter
from .forms import UserForm
from fastapi import Depends
from typing import List


router = APIRouter()
REDIS_URL = "redis://127.0.0.1:6379"

@router.get("/users", response_model=List[UserForm])
async def get_users():
    return await User.all()


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

