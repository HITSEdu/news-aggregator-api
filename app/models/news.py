from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, select
from app.models.database import Base, AsyncSessionLocal
from datetime import datetime
import aiofiles
import json


class News(Base):
    __tablename__ = "News"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    source = Column(String)
    summary_text = Column(String)
    is_green = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())


async def load_initial_news_by_ticker(ticker_name: str):
    filename = f"news/{ticker_name.lower()}.json"
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
