from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserAuth(BaseModel):
    email: EmailStr
    password: str
    

class User(UserAuth):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
