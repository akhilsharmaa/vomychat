from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users
from ..models.referrals import Refrrals
from ..utils.passwords import get_password_hash
from ..utils.users import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="",
    tags=["Refrral"],
    responses={404: {"description": "Not found"}},
)  

class RefrralBase(BaseModel):
    email: str 

@router.post("/referr")
async def create_new_referral(refrral: RefrralBase, db: db_dependency, current_user: Users = Depends(get_current_user)): 

    refrral_body = Refrrals( 
            referrer_user_id=current_user.id,
            referred_user_id=refrral.email,  
        )

    try:

        db.add(refrral_body)
        db.commit()
        db.refresh(refrral_body) 
        
        return JSONResponse(
            status_code=200,
            content={
                    "message": f"Successfully referred", 
                    "detail": f"you have refered the user with email: {current_user.email}, you can check the refrals"
                }
        )

    except IntegrityError as e: 
        
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Failed referred",
                "error": f"Error: {e}"
            }
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed referred. Exception: {str(e)}"
        )



@router.post("/referrals")
async def get_all_refrrals(db: db_dependency, current_user: Users = Depends(get_current_user)): 

    try:

        results = db.query(Refrrals).filter(
                        Refrrals.referrer_user_id == current_user.id).all();  
        
        refered_users_list = []
        for referral in results: 
            refered_users_list.append({
                "referred_user_id": referral.referred_user_id,        
                "status": referral.status,        
            })
        
        return JSONResponse(
            status_code=200,
            content={
                    "message": f"Successfully fetched all the refered user", 
                    "body": f"{refered_users_list}"
                }
        )

    except IntegrityError as e: 

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Failed referred",
                "error": f"Error: {e}"
            }
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed referred. Exception: {str(e)}"
        )
