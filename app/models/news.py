from sqlalchemy import Column, Integer, String, Double, DateTime, func
from sqlalchemy.orm import Session
from . import Base

class News(Base):
    __tablename__ = "News"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column
    source = Column(String)
    summary_text = Column(String)
    timestamp = created_at = Column(DateTime, server_default=func.now())
    @classmethod
    def find_by_ticker(cls, db: Session, ticker: str, limit: int = 10) -> list['News']:
        """
        Находит все новости по тикеру
        :param db: Сессия базы данных
        :param ticker: Тicker для поиска (например, 'AAPL')
        :param limit: Максимальное количество результатов
        :return: Список объектов News
        """
        return db.query(cls).filter(cls.ticker == ticker).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def insert(cls, db: Session, news_data: dict):
        """
        Вставляет новую запись новости
        :param db: Сессия базы данных
        :param news_data: Словарь с данными новости (должен содержать ticker, source, summary_text)
        :return: Созданный объект News
        """
        news_item = cls(
            ticker=news_data['ticker'],
            source=news_data['source'],
            summary_text=news_data['summary_text']
        )
        db.add(news_item)
        db.commit()
        db.refresh(news_item)
        return news_item