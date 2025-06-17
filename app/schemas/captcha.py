from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str
    captcha_token: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    captcha_token: str
