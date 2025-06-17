from sqlalchemy import Column, Integer, String, Double, DateTime, func
from sqlalchemy.orm import relationship

from app.models.database import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Double)
    owner = relationship("Ticker", back_populates="data_items")
    created_at = Column(DateTime, server_default=func.now())
