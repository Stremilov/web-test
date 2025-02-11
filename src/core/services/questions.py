import logging

from aiohttp import ClientSession, ClientError
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.repositories.questions import QuestionRepository
from src.core.schemas.question import QuestionInputData, QuestionResponseData


QUESTION_URL = "https://jservice.io/api/random?count=1"


class QuestionService:

    @staticmethod
    async def get_questions(request: QuestionInputData, db: AsyncSession = Depends(get_db)):
        logging.info(f"Отправлен запрос на получение {request.questions_num} вопросов.")
        async with ClientSession() as session:
            questions = []
            while len(questions) < request.questions_num:
                try:
                    logging.debug(f"Запрос данных на адрес {QUESTION_URL}")
                    async with session.get(QUESTION_URL) as response:
                        if response.status != 200:
                            logging.error(f"Ошибка получения данных. Код ошибки: {response.status}")
                            raise HTTPException(status_code=503, detail="Квиз сервис не доступен")

                        data = await response.json()
                        question_data = data[0]

                        logging.debug(f"Получение данных: {question_data}")

                        if not await QuestionRepository.is_question_exists(db, question_data['id']):
                            await QuestionRepository.save_question(db, question_data)
                            questions.append(question_data)
                            logging.info(f"Сохранен новый вопрос с ID: {question_data['id']}")
                        else:
                            logging.info(f"Вопрос с ID {question_data['id']} уже существует.")
                except ClientError as e:
                    logging.error(f"Ошибка подключения к Квиз сервису: {e}")
                    raise HTTPException(status_code=503, detail="Сервер Квиз недоступен")

        last_question = await QuestionRepository.get_last_question(db)
        if not last_question:
            logging.error("Не было найдено прошлых вопросов в бд")
            raise HTTPException(status_code=404, detail="Вопросы не найдены")

        logging.info(f"Возвращается вопрос с ID: {last_question.id}")

        return QuestionResponseData(
            id=last_question.id,
            question=last_question.question,
            answer=last_question.answer,
            created_at=last_question.created_at.isoformat()
        )


