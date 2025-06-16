from sqlalchemy import Column, Integer, String, Double, DateTime, func
from sqlalchemy.orm import relationship
from . import Base

class Volume(Base):
    __tablename__ = "Volumes"
    id = Column(Integer, primary_key=True, index=True)
    volume = Column(Double)
    owner = relationship("Ticker", back_populates="data_items")
    created_at = Column(DateTime, server_default=func.now())
