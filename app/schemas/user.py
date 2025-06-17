from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class User(UserAuth):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
