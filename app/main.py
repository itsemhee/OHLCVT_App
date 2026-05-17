from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, get_db
from app.models import Base, OHLCVT, User
from app.schemas import OHLCVTCreate, UserCreate
from app.utils import verify, hash
from oauth2 import create_access_token, verify_access_token, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/users")
def login_user(user: UserCreate, db: Session =Depends(get_db), 
               get_current_user: int =Depends(get_current_user)):

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())  #to make things easier 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/{id}")
def get_user(id: int, db: Session= Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()
    
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} was not found")

    return user


@app.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), 
          db: Session = Depends(get_db)):
    
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
    