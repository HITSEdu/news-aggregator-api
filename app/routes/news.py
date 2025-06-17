from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from models.news import News as SQLNews
from schemas.news import NewsOut


router = APIRouter()

@router.get("/get_all_news/{ticker}", response_model=list[NewsOut])
async def get_news_by_ticker(
    ticker: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Получаем данные из БД
    db_news = db.query(SQLNews)\
               .filter(SQLNews.ticker == ticker)\
               .order_by(SQLNews.timestamp.desc())\
               .offset(skip)\
               .limit(limit)\
               .all()
    
    if not db_news:
        raise HTTPException(
            status_code=404,
            detail=f"No news found for ticker {ticker}"
        )
    
    # Преобразуем каждую SQLAlchemy запись в Pydantic модель
    return db_news

@router.get("/get_green_news/{ticker}")
async def get_green_news(ticker: str) -> list[NewsOut]:
    ...

@router.get("/get_red_news/{ticker}")
async def get_red_news(ticker: str) -> list[NewsOut]:
    ...

@router.get("/get_news_by_importance/{ticker}")
async def get_news_by_importance(ticker: str) -> list[NewsOut]:
    ...

@router.get("/get_news_by_source/{ticker}/{src}")
async def get_news_by_source(ticker:str, src: str) -> list[NewsOut]:
    ...

