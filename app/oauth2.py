from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
##SECRET KEY 
## ALGORITHM 
##EXPIRATION TIME 

##the endpoint of the token url is going to be /login and we are going to be using this endpoint in our auth.py file
#OAuth2PasswordBearer is just a helper to grab the token from the Authorization header.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY= settings.secret_key
ALGORITHM= settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    ##we have to set the expiration time for the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = int(expire.timestamp())
    to_encode.update({"exp": expire})
    ##this is important because the token comes back in a int format
    ##this is the same thing as the user id which is technically an int 
    #The schema might have been originally designed for string IDs - But the database and application logic were using integer IDs
    if "user_id" in to_encode:
        to_encode["user_id"] = int(to_encode["user_id"])

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

##we are going to be using this function every single time we want to make an api call to make sure the user is authenticated
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return  user

