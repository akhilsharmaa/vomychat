from datetime import datetime, timedelta, timezone
from typing import Annotated
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

router = APIRouter(
    tags=["Users"],
    responses={404: {"description": "Not found"}},
) 


@router.post("/resend_verification") 
async def read_users_me(db: db_dependency, current_user: Users = Depends(get_current_user)): 

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )

    VERIFY_LINK = f"http://0.0.0.0:8000/verify?token={access_token}"
    BODY_TEXT = f"Please verify you email by clicking on \n {VERIFY_LINK}. or copy and open in browser."     
    
    try: 
        send_mail(subject="Verify you email now", 
                    to=[current_user.email], 
                    body_text=BODY_TEXT); 
        
        
        return JSONResponse(
                status_code=200,
                content= {
                    "message": f"We have sent the verification email to the {current_user.email}",  
                }
            )      

    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        print(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification link"
        )