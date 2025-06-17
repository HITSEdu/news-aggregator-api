from sqlalchemy import Column, Integer, String
from . import Base
from sqlalchemy.orm import relationship


class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prices = relationship("Price", back_populates="owner")
  
