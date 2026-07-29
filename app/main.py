from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models 
from .schemas import PostCreate,Post,UserCreate,UserOut
from .database import engine, get_db
from .swagger import get_dark_swagger_ui_html
from sqlalchemy.orm import Session
from typing import List
from .utils import hash
from .routers import user,post,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_dark_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
    )



while(True):
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'posts',user = 'postgres',password = 'abc123**',cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("DB Connected")
        break
    except Exception as error: 
        print("DB connection failed")
        print("Error: ", error)
        time.sleep(2)

    




    
