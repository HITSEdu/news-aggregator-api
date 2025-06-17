from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str



class UserAuth(UserBase):
    captcha_token: str
    login: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


market_twist_tags = {"GAZP": ["газ", "нефть"]}
rbk_tags = ["GAZP"]
