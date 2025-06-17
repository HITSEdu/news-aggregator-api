from pydantic import BaseModel

class NewsOut(BaseModel):
    ticker: str
    source: str
    summary_text: str
    # abs(price(news.timestamp - 1 hour) - price(news.timestamp + 1 hour))
    price_diffrence: str  # Обратите внимание на опечатку: возможно, вы имели в виду price_difference
    timestamp: str  # Или используйте datetime, если хотите работать с датами
    
    class Config:
        orm_mode = True 