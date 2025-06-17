from dotenv import load_dotenv 
from pydantic import BaseConfig, HttpUrl

load_dotenv()

class Config(BaseConfig):
    yandex_api_token: str
    yandex_api_url: HttpUrl

config = Config()