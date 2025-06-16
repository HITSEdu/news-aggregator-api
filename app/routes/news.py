from fastapi import APIRouter
from models.news import News

router = APIRouter()

@router.get("/get_all_news/{ticker}")
async def get_news_by_ticker(ticker: str):
    ...

@router.get("/get_green_news/{ticker}")
async def get_green_news(ticker: str):
    ...

@router.get("/get_red_news/{ticker}")
async def get_red_news(ticker: str):
    ...

@router.get("/get_news_by_importance/{ticker}")
async def get_news_by_importance(ticker: str):
    ...

@router.get("/get_news_by_source/{ticker}/{src}")
async def get_news_by_source(ticker:str, src: str):
    ...

