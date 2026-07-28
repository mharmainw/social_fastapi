from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models 
from ..schemas import PostCreate,Post,UserCreate,UserOut
from ..database import engine, get_db
from ..swagger import get_dark_swagger_ui_html
from sqlalchemy.orm import Session
from typing import List
from ..utils import hash



router = APIRouter(
    prefix = '/users',
    tags = ['Users']
)

@router.post('/',status_code = status.HTTP_201_CREATED,response_model= UserOut)
async def createuser(user: UserCreate,db:Session= Depends(get_db)):

    hashed_pwd = hash(user.password)
    user.password = hashed_pwd
    user_dict = user.model_dump()

    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=UserOut)
async def getuser(id: int, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'user with id: {id} was not found')

    return user
