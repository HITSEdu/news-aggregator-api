from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.price import Price
from math import fabs


async def get_price_difference(db: AsyncSession, timestamp: datetime) -> float:
    timestamp_plus_1h = timestamp + timedelta(hours=1)
    timestamp_minus_1h = timestamp - timedelta(hours=1)
    stmt = (
        select(Price)
        .where(
            Price.timestamp >= timestamp_minus_1h,
            Price.timestamp <= timestamp_plus_1h,
        )
        .options(selectinload(Price.owner))
        .order_by(Price.timestamp)
    )
    result = await db.execute(stmt)
    prices = result.scalars().all()
    return fabs(prices[0] - prices[-1])
