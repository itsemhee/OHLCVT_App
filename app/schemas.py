from pydantic import BaseModel
from datetime import datetime

class OHLCVTCreate(BaseModel):
    timestamp : datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trades: int