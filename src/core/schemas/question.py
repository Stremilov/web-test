from pydantic import BaseModel


class QuestionInputData(BaseModel):
    questions_num: int


class QuestionResponseData(BaseModel):
    id: int
    question: str
    answer: str
    created_at: str

