from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi import Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..schemas import UserCreate, UserOut


router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# #creating our user row entry in the user table 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:

        ##first we will hash the password 
        ## getting it from user.password
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        print(f"Attempting to create user with data: {user.dict()}")
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Successfully created user: {new_user}")
        return new_user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail=f"Error creating user: {str(e)}")

#getting information about a specific user 
@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user

