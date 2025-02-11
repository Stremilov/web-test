from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import QuizQuestion


class QuestionRepository:

    @staticmethod
    async def get_last_question(db: AsyncSession):
        result = await db.execute(select(QuizQuestion).order_by(QuizQuestion.id.desc()))
        return result.scalars().first()

    @staticmethod
    async def save_question(db: AsyncSession, question_data: dict):
        question = QuizQuestion(
            question_id=question_data['id'],
            question=question_data['question'],
            answer=question_data['answer'],
            created_at=question_data['created_at']
        )
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question

    @staticmethod
    async def is_question_exists(db: AsyncSession, question_id: int):
        result = await db.execute(select(QuizQuestion).filter(QuizQuestion.question_id == question_id))
        return result.scalars().first() is not None
