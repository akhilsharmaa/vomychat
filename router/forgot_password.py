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
        
@router.get("/changepassword")
async def verify_email_user(db: db_dependency, token: str, new_password: str): 

    if(token == None ): 
        return JSONResponse(
                status_code=401,
                content= {
                    "message": f"please provide a valid token",  
                }
            )    
        
    if(new_password == None or len(new_password) <= 8): 
        return JSONResponse(
                status_code=401,
                content= {
                    "message": f"please provide a valid new password, greater then 8 digits.",  
                }
            )    


    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None: 
            return JSONResponse(
                status_code=401,
                content= {
                    "message": f"Verificaiton link expired. ",  
                }
            )    
    
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid Token, Failed to decode the token {str(e)}"
        )
        
    
    try:

        referrer_user = db.query(Users).filter(Users.username == username).first()
        
        if referrer_user is None: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification link, No user found"
            )

        referrer_user.password = new_password; 
        db.commit()  # Commit the changes
        db.refresh(referrer_user)  # Refresh the session to reflect changes

            
        return JSONResponse(
                    status_code=200,
                    content= {
                        "message": f"we have successfully changed the password",  
                    }
                )   

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify email. Exception: {str(e)}"
        )
        