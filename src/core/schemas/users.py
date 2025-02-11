from pydantic import BaseModel


class CreateUserData(BaseModel):
    username: str
