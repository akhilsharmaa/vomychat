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
        

@router.get("/getpasswordresetemail") 
async def read_users_me(db: db_dependency, email: str): 
 
    try: 
        current_user = db.query(Users).filter(Users.email == email).first(); 
        
        if(current_user is None): 
            return JSONResponse(
                    status_code=401,
                    content= {
                        "message": f"No account associated with email {email}",  
                    }
                )      

    except Exception as e: 
        print(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send password changing email"
        )
        

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )

    VERIFY_LINK = f"{BASE_API}/api/changepassword?token={quote(access_token)}&new_password="
    BODY_TEXT = (
        f"Click the link below to reset your password:\n\n"
        f"{VERIFY_LINK}\n\n"
        f"If the above link doesn't work, you can make a GET request with the following details:\n\n"
        f"- Token: `{quote(access_token)}`\n"
        f"- New Password: (Provide your new password in the request)"
    )

    try: 
        send_mail(subject="Reset Password", 
                    to=[current_user.email], 
                    body_text=BODY_TEXT);  
        
    except Exception as e: 
        print(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification link"
        )
        
        

    return JSONResponse(
                status_code=200,
                content= {
                    "message": f"We have sent the reset password email to the {current_user.email}",  
                }
            )
    