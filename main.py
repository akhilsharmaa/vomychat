import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from .router import users, auth
from .services.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from .utils.logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router) 
app.include_router(auth.router)  

create_tables()

@app.get("/")
async def root():
    logger.info(f"New Request at '/' ")

    return {
                "message": "welcome to server",
            }