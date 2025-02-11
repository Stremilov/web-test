from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.connection import Base


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class AudioRecord(Base):
    __tablename__ = 'audio_records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    uuid: Mapped[str] = mapped_column(String, unique=True, nullable=False)