from fastapi import Form, UploadFile, File, APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.services.audios import AudioService

audio_router = APIRouter(
    tags=["Audio service"]
)


@audio_router.post("/upload_audio")
async def upload_audio(
        user_id: int = Form(...),
        token: str = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)):
    return await AudioService.upload_audio(user_id, token, file, db)


@audio_router.get("/record")
async def download_audio(audio_id: int = Query(...), user: int = Query(...), db: AsyncSession = Depends(get_db)):
    return await AudioService.download_audio(audio_id, user, db)
