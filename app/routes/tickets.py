from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db
from app.models.ticker import Ticker
from app.schemas.ticker import TickerResponse

router = APIRouter()


@router.get("/test/tickers", response_model=list[TickerResponse])
async def get_all_tickers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticker))
    tickers = result.scalars().all()
    return tickers
