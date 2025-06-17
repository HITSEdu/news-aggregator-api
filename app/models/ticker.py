from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prices = relationship("Price", back_populates="owner")
  
