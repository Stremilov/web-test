from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.connection import get_db
from src.core.schemas.question import QuestionResponseData, QuestionInputData
from src.core.services.questions import QuestionService

quiz_router = APIRouter(
    prefix="/quiz"
)


@quiz_router.post(
    path="/",
    response_model=QuestionResponseData,
    tags=["Questions"],
    summary="Возвращает вопросы для викторины",
    description="""
    - Принимает на вход запросы с содержимым вида {"questions_num": integer}
    - После получения запроса запрашивает с публичного API 
    - Результат запроса с API сохраняется в бд, если такой результат запроса уже есть, то запрос выполняется снова
    - Возвращает предыдущий вопрос для викторины
    """
)
async def get_quiz_questions(data: QuestionInputData, db: AsyncSession = Depends(get_db)):
    return await QuestionService.get_questions(data, db)
