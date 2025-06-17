from fastapi import APIRouter, Depends, HTTPException
from app.tinkoff_client.get_price_by_ticker import get_monthly_hourly_candles
from app.models.price import Price

router = APIRouter()

@router.get("/price/sber")
async def get_price_sber():
    result = await get_monthly_hourly_candles("GAZP")
    
    return result