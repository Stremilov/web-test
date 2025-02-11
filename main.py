import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from src.api.quiz import quiz_router
from src.core.database.connection import engine, Base
from src.core.utils.config import settings

app = FastAPI(root_path="")

app.include_router(quiz_router)

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.debug("База данных создана")


async def main() -> None:
    uvicorn.run(
        "main:app",
        port=settings.run.port,
        host=settings.run.host,
        reload=True
    )

if __name__ == "__main__":
    asyncio.run(main())
