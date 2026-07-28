
from pydantic import BaseModel, ConfigDict,EmailStr

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