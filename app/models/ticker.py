from sqlalchemy import Column, Integer, String
from sqlalchemy import select

from app.models.database import AsyncSessionLocal
from app.models.database import Base


class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


async def create_initial_tickers():
    async with AsyncSessionLocal() as db:
        ticker_names = ["GZPR", "LKOH", "SBER", "T", "VTBR", "YDEX"]
        existing_tickers = await db.execute(select(Ticker.name))
        existing_names = {name for (name,) in existing_tickers.all()}
        new_tickers = []
        for name in ticker_names:
            if name not in existing_names:
                new_ticker = Ticker(name=name)
                db.add(new_ticker)
                new_tickers.append(new_ticker)

        await db.commit()
        for ticker in new_tickers:
            await db.refresh(ticker)

        return new_tickers


async def get_tickers() -> list[Ticker]:
    async with AsyncSessionLocal() as db:
        # return ["GZPR", "LKOH", "SBER", "T", "VTBR", "YDEX"]
        result = await db.execute(select(Ticker))
        tickers = result.scalars().all()
        return tickers
