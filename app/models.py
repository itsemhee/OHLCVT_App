from sqlalchemy import Column, DateTime, Integer, BigInteger, Double, String
from app.database import Base

class OHLCVT (Base):
    __tablename__ = "ohlcvt"

    timestamp = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Double)
    high = Column(Double)
    low = Column(Double)
    close = Column(Double)
    volume = Column(Double)
    trades = Column(BigInteger)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)