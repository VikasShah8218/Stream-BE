from app.accounts.auth import authenticate_user, create_access_token
from app.accounts.forms import LoginRequestForm,UserRegisterForm
from app.accounts.auth import get_password_hash
from fastapi import APIRouter, HTTPException
from datetime import timedelta
from .models import User

router = APIRouter()

@router.post("/login")
async def login(payload: LoginRequestForm):
    user = await authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/register")
async def register(user: UserRegisterForm):
    existing_user = await User.get_or_none(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = get_password_hash(user.password)

    new_user = await User.create(
        username=user.username,
        email=user.email,
        password=hashed_pw,
    )
    return {"message": f"User {new_user.username} created successfully"}

