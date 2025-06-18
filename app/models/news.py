import json
import logging
from datetime import datetime

import aiofiles
from select import select
from sqlalchemy import Column, Integer, String, DateTime, func, Text, Boolean
from app.models.database import AsyncSessionLocal, Base
from app.utils.config import config


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), nullable=False)
    source = Column(String(255), nullable=False)
    summary_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    price_difference = Column(String(50), nullable=False)
    is_green = Column(Boolean, nullable=False, server_default='false')


async def load_initial_news_by_ticker(ticker_name: str):
    filename = f"{config.path_to_data}{ticker_name}.json"
    async with AsyncSessionLocal() as session:
        try:
            async with aiofiles.open(filename, mode="r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)
            for item in data:
                existing_news = await session.execute(
                    select(News).where(
                        News.summary_text == item["summary_text"],
                        News.created_at == datetime.fromisoformat(item["timestamp"]),
                    )
                )
                if not existing_news.scalar_one_or_none():
                    news = News(
                        ticker=item["ticker"],
                        source=item["source"],
                        summary_text=item["summary_text"],
                        created_at=datetime.fromisoformat(item["timestamp"]),
                        price_difference=item["price_difference"],
                        is_green=bool(item["is_green"]),
                    )
                    session.add(news)
            await session.commit()
            return {
                "status": "success",
                "message": f"News for {ticker_name} loaded successfully",
            }

        except FileNotFoundError:
            return {"status": "error", "message": f"File {filename} not found"}
        except json.JSONDecodeError:
            return {"status": "error", "message": f"File {filename} is not valid JSON"}
        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}
