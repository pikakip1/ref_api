import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.user.auth import auth_backend
from src.user.models import User
from src.user.manager import get_user_manager
from src.user.schemas import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user/jwt",
    tags=["user"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/user",
    tags=["user"],
)
