from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class News(BaseModel):
    ticker: str
    source: str
    summary_text: str
    price_diffrence: str
    timestamp: str
