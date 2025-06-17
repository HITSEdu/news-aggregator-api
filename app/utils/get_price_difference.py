from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from models.ticker import Ticker
from models.price import Price


async def get_price_difference(db: AsyncSession, timestamp: datetime):
    # Рассчитываем временные границы
    timestamp_plus_1h = timestamp + timedelta(hours=1)
    timestamp_minus_1h = timestamp - timedelta(hours=1)

    # Строим асинхронный запрос
    stmt = (
        select(Price)
        .join(Ticker)
        .where(
            Price.created_at >= timestamp_minus_1h,
            Price.created_at <= timestamp_plus_1h,
        )
        .options(selectinload(Price.owner))  # Жадная загрузка связанного тикера
    )

    # Выполняем запрос
    result = await db.execute(stmt)
    prices = result.scalars().all()

    # Форматируем результаты
    return [
        {
            "id": price.id,
            "price": price.price,
            "created_at": price.created_at,
            "ticker_name": price.owner.name,  # Доступ через relationship
        }
        for price in prices
    ]
