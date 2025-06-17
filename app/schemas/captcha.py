from pydantic import BaseModel


# Модель запроса (добавляем captcha_token
class LoginRequest(BaseModel):
    email: str
    password: str
    captcha_token: str  # Токен reCAPTCHA с фронтенда


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    captcha_token: str  # Токен reCAPTCHA с фронтенда
