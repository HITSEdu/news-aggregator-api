from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class User(UserCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
