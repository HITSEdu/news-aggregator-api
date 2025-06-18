from pydantic import BaseModel


class NewsOut(BaseModel):
    ticker: str
    source: str
    summary_text: str
    price_difference: str
    is_green: bool
    timestamp: str

    class Config:
        orm_mode = True
