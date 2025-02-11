from uuid import uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.database.models import User


class UserService:

    @staticmethod
    async def create_user(username: str, db: AsyncSession):
        token = str(uuid4())
        new_user = User(username=username, token=token)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"user_id": new_user.id, "token": new_user.token}
