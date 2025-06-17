import json
from datetime import datetime

import aiofiles
from select import select
from sqlalchemy import Column, Double, String, DateTime, func, Integer

from app.models.database import AsyncSessionLocal
from app.models.database import Base
from app.utils.get_price_difference import get_price_difference
import logging


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column
    source = Column(String)
    summary_text = Column(String)
    price_difference = Column(Double)
    created_at = Column(DateTime, server_default=func.now())


async def load_initial_news_by_ticker(ticker_name: str):
    logging.error(f"LOADING NEWS FOR", ticker_name)
    filename = f"news/{ticker_name.lower()}.json"
    async with AsyncSessionLocal() as session:
        try:
            async with aiofiles.open(filename, mode="r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)
                logging.error("DATA", data)

            for item in data:
                existing_news = await session.execute(
                    select(News).where(
                        News.summary_text == item["summary_text"],
                        News.created_at == datetime.fromisoformat(item["timestamp"]),
                    )
                )
                if not existing_news.scalar_one_or_none():
                    # price_difference = get_price_difference(
                    #     session, timestamp=parse_timestamp(item["timestamp"])
                    # )
                    news = News(
                        ticker=item["ticker"],
                        source=item["source"],
                        summary_text=item["summary_text"],
                        created_at=datetime.fromisoformat(item["timestamp"]),
                        price_difference=1.2,
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


def parse_timestamp(timestamp_str: str) -> datetime:
    return datetime.datetime.fromisoformat(timestamp_str)
