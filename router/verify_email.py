from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import quote
import jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users 
from ..models.referrals import Refrrals, ReferralStatus 
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


@router.post("/email-verification") 
async def read_users_me(db: db_dependency, current_user: Users = Depends(get_current_user)): 

    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )

    VERIFY_LINK = f"{BASE_API}/api/verify?token={quote(access_token)}"
    BODY_TEXT = f"Please verify you email by clicking on \n {VERIFY_LINK}. or copy and open in browser."     
    
    print(BODY_TEXT)
    
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
        print(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification link"
        )
        
        
@router.get("/verify")
async def verify_email_user(db: db_dependency, token: str):

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
            detail=f"Failed to decode the token {str(e)}"
        )
            
    
    # TODO: update the refrrals table when user verified, the token pending -> completed. 
    
    try:
        referrer_user = db.query(Users).filter(Users.username == username).first()

        if referrer_user is None: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification link, No user found"
            )

        referrer_user.is_email_verified = True
        db.commit()  # Commit the changes
        db.refresh(referrer_user)  # Refresh the session to reflect changes


    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify email. Exception: {str(e)}"
        )
    
    
    try:
        referral = db.query(Refrrals).filter(Refrrals.referred_user_id == str(referrer_user.id)).first()
        
        print(referral)
        
        if referral: 
            referral.status = ReferralStatus.SUCCESSFUL; 
            db.commit()  # Commit the changes
            db.refresh(referral)  # Refresh the session to reflect changes

    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update refrals, please try again later. {str(e)}"
        )
        
            
    return JSONResponse(
                    status_code=200,
                    content= {
                        "message": f"we have successfully verified you, thankyou",  
                    }
                )   