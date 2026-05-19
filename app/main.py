from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, get_db
from app.models import Base, OHLCVT, User
from app.schemas import OHLCVTCreate, UserCreate
from app.utils import verify, hash
from app.oauth2 import create_access_token, verify_access_token, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/users")
def login_user(user: UserCreate, db: Session =Depends(get_db), 
               get_current_user: int =Depends(get_current_user)):
    
    logger.info("Creating new User")

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())  #to make things easier 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User with id {new_user.id}")

    return new_user

@app.get("/users/{id}")
def get_user(id: int, db: Session= Depends(get_db)):

    logger.info(f"Fetching User With id {id}")

    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} was not found")
    
    logger.info(f"User with id {id} fetched successfully")

    return user


@app.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), 
          db: Session = Depends(get_db)):
    
    logger.info(f"Login attempt for {user_credentials.username}")

    {
        "username": "asfjn",
        "password": "yjrderdtfygk"
    }

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
    
    access_token = create_access_token(data= {"user_id": user.id})

    logger.info(f"User {user.id} logged in successfully")

    return{"access_token": access_token, "token_type": "bearer"}

@app.post("/insert")
def insert_data(data: OHLCVTCreate, db: Session= Depends(get_db)):


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
    