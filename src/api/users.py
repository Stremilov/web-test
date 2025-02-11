from fastapi import APIRouter, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.schemas.users import CreateUserData
from src.core.services.users import UserService

users_router = APIRouter(
    prefix="",
    tags=["Audio service"]
)


@users_router.post("/create_user")
async def create_user(data: CreateUserData, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(data.username, db)


