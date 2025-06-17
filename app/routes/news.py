from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.database import get_db
from app.models.news import News as SQLNews
from app.schemas.news import NewsOut

router = APIRouter()


@router.get("/news/{ticker_id}", response_model=NewsOut)
async def get_news_by_ticker(ticker_id: int, db: AsyncSession = Depends(get_db)):
    # Используем await с execute для асинхронного запроса
    result = await db.execute(select(SQLNews).filter(SQLNews.id == ticker_id))
    news = result.scalars().first()

    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    return news
