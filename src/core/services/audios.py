import logging
import os
import shutil
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydub import AudioSegment
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import User, AudioRecord
from src.core.utils.config import settings

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


class AudioService:

    @staticmethod
    async def upload_audio(
            user_id: int,
            token: str,
            file: UploadFile,
            db: AsyncSession
    ):
        logging.info(f"Начало загрузки аудио для пользователя {user_id}")
        user = await db.get(User, user_id)
        if not user or user.token != token:
            logging.warning(f"Ошибка авторизации для пользователя {user_id}")
            raise HTTPException(status_code=403, detail="Неправильный ID пользователя или токен")

        wav_path = os.path.join(UPLOAD_DIR, f"{uuid4()}.wav")
        mp3_path = wav_path.replace(".wav", ".mp3")

        logging.info(f"Сохранение WAV файла по пути: {wav_path}")
        with open(wav_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            logging.info(f"Конвертация файла {wav_path} в MP3")
            audio = AudioSegment.from_wav(wav_path)
            audio.export(mp3_path, format="mp3")
            logging.info(f"Файл успешно конвертирован и сохранён по пути: {mp3_path}")
        except Exception as e:
            logging.error(f"Ошибка при конвертации файла: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ошибка при конвертации файла: {str(e)}")

        record_uuid = str(uuid4())
        new_record = AudioRecord(user_id=user_id, file_path=mp3_path, uuid=record_uuid)
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)

        logging.info(f"Аудиозапись сохранена в базе данных с ID {new_record.id}")
        return {"download_url": f"http://{settings.run.host}:{settings.run.port}/record?audio_id={new_record.id}&user={user_id}"}

    @staticmethod
    async def download_audio(audio_id: int, user_id: int, db: AsyncSession):
        logging.info(f"Запрос на скачивание аудио с ID {audio_id} для пользователя {user_id}")
        record = await db.get(AudioRecord, audio_id)
        if not record or record.user_id != user_id:
            logging.warning(f"Аудиозапись с ID {audio_id} не найдена для пользователя {user_id}")
            raise HTTPException(status_code=404, detail="Такого аудио нет")

        logging.info(f"Предоставление доступа к файлу {record.file_path}")
        return FileResponse(record.file_path, media_type='audio/mpeg', filename=os.path.basename(record.file_path))