from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import quote
import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users 
from ..utils.users import get_current_user
from fastapi.responses import JSONResponse
from ..services.claim_refrral import claim_new_refrral_by
from typing import Optional
from ..services.send_mail import send_mail
from ..utils.passwords import create_access_token
from ..config import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context, BASE_API

router = APIRouter(
    prefix="/api",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
) 
        
@router.get("/forgotpassword")
async def verify_email_user(db: db_dependency, token: str):
        
    return JSONResponse(
                    status_code=200,
                    content= {
                        "message": f"we have successfully verified you, thankyou",  
                    }
                )   