import json

import aiofiles
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.news import News as SQLNews
from app.schemas.news import NewsOut
from app.utils.config import config

news_router = APIRouter()


@news_router.get("/get_all_news/{ticker}", response_model=list[NewsOut])
async def get_news_by_ticker(
        ticker: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    db_news = db.query(SQLNews) \
        .filter(SQLNews.ticker == ticker) \
        .order_by(SQLNews.timestamp.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()

    if not db_news:
        raise HTTPException(
            status_code=404,
            detail=f"No news found for ticker {ticker}"
        )
    return db_news


@news_router.get("/get_all_news")
async def get_news_by_ticker():
    filenames = [
        "sber.json",
        "gzpr.json",
        "lkoh.json",
        "t.json",
        "ydex.json",
        "vtbr.json"
    ]
    combined_data = []
    for filename in filenames:
        async with aiofiles.open(f"{config.path_to_data}{filename}", mode="r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)
            combined_data.extend(data)
    return combined_data
