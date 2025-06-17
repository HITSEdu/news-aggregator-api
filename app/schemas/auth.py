from pydantic import BaseModel

from app.schemas.user import UserWithTicker


class Token(BaseModel):
    token: str
    refreshToken: str
    user: UserWithTicker


class TokenData(BaseModel):
    username: str | None = None
