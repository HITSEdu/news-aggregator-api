from fastapi import APIRouter

from app.tinkoff_client.get_price_by_ticker import get_monthly_hourly_candles

router = APIRouter()


@router.get("/price/sber")
async def get_price_sber():
    result = await get_monthly_hourly_candles("GAZP")

    return result
