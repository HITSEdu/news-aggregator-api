from sqlalchemy import Column, Integer, String, Double, DateTime, func
from . import Base

class News(Base):
    __tablename__ = "News"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column
    source = Column(String)
    summary_text = Column(String)
    timestamp = created_at = Column(DateTime, server_default=func.now())
