from fastapi import APIRouter

from app.tinkoff_client.get_price_by_ticker import get_monthly_hourly_candles

router = APIRouter()


@router.get("/price/{ticker}")
async def get_price(ticker: str):
    result = await get_monthly_hourly_candles(ticker)
    return result
