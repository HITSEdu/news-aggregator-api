import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    yandex_api_token: str = os.getenv("YANDEX_API_TOKEN")
    yandex_api_url: str = os.getenv("YANDEX_API_URL")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = os.getenv("DATABASE_URL")
    tinkoff_api_token: str = os.getenv("TINKOFF_API_TOKEN")
    recaptcha_secret_key: str = os.getenv("RECAPTCHA_SECRET_KEY")
    recaptha_site_key: str = os.getenv("RECAPTCHA_SITE_KEY")
    telegram_account_api_id: int = os.getenv("TELEGRAM_ACCOUNT_API_ID")
    telegram_api_hash: str = os.getenv("TELEGRAM_API_HASH")
    path_to_data: str = os.getenv("PATH_TO_DATA")


config = Config()
