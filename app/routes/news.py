from fastapi import APIRouter
from models.news import News

router = APIRouter()

@router.get("/get_news_by_ticker")
async def get_news_by_ticker(ticker: str):
    ...

@router.get("/get_x")