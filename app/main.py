from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, OHLCVT
from app.schemas import OHLCVTCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/insert") 
def insert_data(data: OHLCVTCreate):

    db = SessionLocal

    new_record = OHLCVT(
        timestamp = data.timestamp,
        open= data.open,
        high = data.high,
        low = data.low,
        close = data.close,
        volume = data.volume,
        trades= data.trades
    )

    db.add(new_record)
    db.commit()

    return{"Message": "Data Inserted Successfully"}

@app.get("/data")
def get_data() :
    db = SessionLocal()
    records = db.query(OHLCVT).limit(100).all()
    return records          