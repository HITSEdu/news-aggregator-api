from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class UserWithTicker(BaseModel):
    email: EmailStr
    login: str
    tickers: List[str]


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserAuth(UserBase):
    captchaToken: str
    login: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


market_twist_tags = {"GAZP": ["газ", "нефть"]}
rbk_tags = ["GAZP"]
