from fastapi import FastAPI
from . import models 
from .database import engine
from .swagger import get_dark_swagger_ui_html
from .routers import user,post,auth,vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# tells sql alchemy to run create statement to generate tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# websites that can access your api
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Social FastAPI is running",
        "docs": "/docs",
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_dark_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
    )


    




    
