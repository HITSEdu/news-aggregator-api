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


@router.get("/get_news_by_importance/{ticker}")
async def get_news_by_importance(ticker: str) -> list[NewsOut]:
    ...


@router.get("/get_news_by_source/{ticker}/{src}")
async def get_news_by_source(ticker: str,
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
