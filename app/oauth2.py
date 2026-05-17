import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from config import settings

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update ({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
       payload = jwt.decode(token, settings.SECRET_KEY, algorithms= [settings.ALGORITHM])

       id = payload.get("user_id")
 
       if id is None:
           raise credentials_exception
       token_data = schemas.TokenData(id= id)

    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str= Depends(OAuth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
