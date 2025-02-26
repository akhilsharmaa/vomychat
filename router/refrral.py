from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users
from ..models.referrals import Refrrals
from ..utils.passwords import get_password_hash
from ..utils.users import get_current_user
from fastapi.responses import JSONResponse
from sqlalchemy import cast, String

router = APIRouter(
    prefix="/api",
    tags=["Refrral"],
    responses={404: {"description": "Not found"}},
)


@router.post("/referrals")
async def get_all_refrrals(db: db_dependency, current_user: Users = Depends(get_current_user)): 

    try:

        results = db.query(Refrrals).where(
            cast(Refrrals.referrer_user_id, String) == str(current_user.id)
        ).all()
        
        refered_users_list = []
        for referral in results: 
            refered_users_list.append({        
                "user_id": referral.referred_user_id,        
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
