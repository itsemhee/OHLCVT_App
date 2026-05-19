from pydantic import BaseModel, EmailStr
from datetime import datetime

class OHLCVTCreate(BaseModel):
    timestamp : datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trades: int

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    created_at: datetime