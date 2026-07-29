
from pydantic import BaseModel, ConfigDict,EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass 


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id : int
    created_at: datetime

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email : EmailStr
    created_at : datetime


class UserLogin(BaseModel):
    email : EmailStr
    password : str



class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str] = None