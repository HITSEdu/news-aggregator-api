from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.news import News as SQLNews
from app.schemas.news import NewsOut

router = APIRouter()


@router.get("/get_all_news/{ticker}", response_model=list[NewsOut])
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


@router.get("/green/{ticker}", response_model=list[NewsOut])
async def get_green_news(
        ticker: str,
        min_importance: int = 0,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[NewsOut]:
    query = db.query(SQLNews).filter(
        SQLNews.ticker == ticker,
        SQLNews.sentiment_score > 0,
        SQLNews.importance >= min_importance,
    )
    green_news = query.order_by(SQLNews.timestamp.desc()).offset(skip).limit(limit).all()
    if not green_news:
        raise HTTPException(status_code=404, detail=f"No green news found for ticker {ticker}")
    return green_news


@router.get("/red/{ticker}", response_model=list[NewsOut])
async def get_red_news(
        ticker: str,
        max_importance: int | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[NewsOut]:
    filters = [SQLNews.ticker == ticker, SQLNews.sentiment_score < 0]
    if max_importance is not None:
        filters.append(SQLNews.importance <= max_importance)
    query = db.query(SQLNews).filter(*filters)
    red_news = query.order_by(SQLNews.timestamp.desc()).offset(skip).limit(limit).all()
    if not red_news:
        raise HTTPException(status_code=404, detail=f"No red news found for ticker {ticker}")
    return red_news


@router.get("/get_news_by_importance/{ticker}")
async def get_news_by_importance(ticker: str) -> list[NewsOut]:
    ...


@router.get("/get_news_by_source/{ticker}/{src}")
async def get_news_by_source(        ticker: str,
        src: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[NewsOut]:
    source_news = (
        db.query(SQLNews)
        .filter(SQLNews.ticker == ticker, SQLNews.source == src)
        .order_by(SQLNews.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not source_news:
        raise HTTPException(status_code=404, detail=f"No news found for ticker {ticker} from source {src}")
    return source_news


@router.get("/price/sber")
async def get_price_sber():
    ...
    # return get_price_by_ticker()
