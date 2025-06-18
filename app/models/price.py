from datetime import timezone

from sqlalchemy import Column, Integer, Double, DateTime, select

from app.models.database import AsyncSessionLocal
from app.models.database import Base
from app.tinkoff_client.get_price_by_ticker import get_monthly_hourly_candles


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Double)
    ticker_id = Column(Integer, index=True)
    timestamp = DateTime(timezone=True)


async def load_prices_for_ticker(ticker: str, ticker_id: int):
    prices = await get_monthly_hourly_candles(ticker)
    async with AsyncSessionLocal() as db:
        for price_data in prices:
            existing = await db.execute(
                select(Price).where(
                    Price.ticker_id == ticker_id, Price.timestamp == price_data["time"]
                )
            )
            timestamp = price_data["time"].astimezone(timezone.utc)
            if not existing.scalar_one_or_none():
                db_price = Price(
                    price=price_data["value"],
                    ticker_id=ticker_id,
                    timestamp=timestamp,
                )
                db.add(db_price)

        await db.commit()
