import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from .router import users, auth, refrral, verify_email, forgot_password, send_password_reset_email
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
app.include_router(refrral.router)  
app.include_router(verify_email.router)  
app.include_router(forgot_password.router)  
app.include_router(send_password_reset_email.router)  

create_tables()

@app.get("/")
async def root():
    logger.info(f"New Request at '/' ")

    return {
                "message": "welcome to server",
            }