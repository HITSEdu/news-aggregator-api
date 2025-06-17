from datetime import datetime, timedelta

from app.models.price import Price
from app.models.ticker import Ticker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def get_price_difference(db: AsyncSession, timestamp: datetime):
    timestamp_plus_1h = timestamp + timedelta(hours=1)
    timestamp_minus_1h = timestamp - timedelta(hours=1)
    stmt = (
        select(Price)
        .join(Ticker)
        .where(
            Price.timestamp >= timestamp_minus_1h,
            Price.timestamp <= timestamp_plus_1h,
        )
        .options(selectinload(Price.owner))
    )
    result = await db.execute(stmt)
    prices = result.scalars().all()
    return [
        {
            "id": price.id,
            "price": price.price,
            "created_at": price.created_at,
            "ticker_name": price.owner.name,
        }
        for price in prices
    ]
