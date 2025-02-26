from ..services.database import db_dependency
from ..models import referrals
from ..models.referrals import Refrrals
from ..models.users import Users
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

def claim_new_refrral_by(referrer:str, referred:str, db:db_dependency):
    
    try:
        referrer_user = db.query(Users).filter(Users.username == referrer).first();
        print(referrer_user.id);  
        
        if(referrer_user == None): 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invaild refrral, please check your refrral"
            )
            
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed referred. Exception: {str(e)}"
        )
        
    refrral_body = Refrrals( 
        referrer_user_id=referrer_user.id,
        referred_user_id=referred,  
    )

    try:
        db.add(refrral_body)
        db.commit()
        db.refresh(refrral_body)

    except IntegrityError as e: 

        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f"You have already referred {referred}, there is no need of referr again." 
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed referred. Exception: {str(e)}"
        )