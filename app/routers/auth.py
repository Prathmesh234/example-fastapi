from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import database, models, schemas, oauth2
from .. import utils
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login( user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    ## OAuth2PasswordRequestForm will automatically take care of the parsing of the form data in this form  {"username": "which is the email for us", "password": "password"}
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    ##create a token for the user 
    ##and return the token for the user 

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
