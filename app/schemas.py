from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from pydantic import EmailStr, Field
from annotated_types import Ge, Le
from typing import Optional
Base = declarative_base()

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
        ##this is going to tell pydantic to convert the sql alchemy object into a dict so we can use it in our response model 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id:int
    dir: int = Field(ge=0, le=1) ##this is going to be a 0 or 1 value



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True


