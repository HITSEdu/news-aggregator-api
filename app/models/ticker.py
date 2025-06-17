from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import select
from app.models.database import AsyncSessionLocal
from app.models.database import Base


class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


async def create_initial_tickers():
    async with AsyncSessionLocal() as db:
        ticker_names = [
            "YNDX",
            "GAZP",
            "TCSG",
            "SBER",
            "MTSS",
            "ROSN",
            "VTBR",
            "VKCO",
            "CHMF",
            "GMKN",
        ]

        # Проверяем, есть ли уже тикеры в базе
        existing_tickers = await db.execute(select(Ticker.name))
        existing_names = {name for (name,) in existing_tickers.all()}

        # Создаем только отсутствующие тикеры
        new_tickers = []
        for name in ticker_names:
            if name not in existing_names:
                new_ticker = Ticker(name=name)
                db.add(new_ticker)
                new_tickers.append(new_ticker)

        await db.commit()

        # Обновляем объекты, чтобы получить их ID
        for ticker in new_tickers:
            await db.refresh(ticker)

        return new_tickers
