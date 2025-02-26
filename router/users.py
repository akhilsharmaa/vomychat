from datetime import datetime, timedelta, timezone
from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users
from ..utils.passwords import get_password_hash
from ..utils.users import get_current_user
from fastapi.responses import JSONResponse
from ..services.claim_refrral import claim_new_refrral_by
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
) 


class UserBase(BaseModel): 
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


@router.post("/register")
async def create_user( user: UserBase, db: db_dependency, referrer: Optional[str] = None):

    
    # TODO: Validate the users emails and username

    new_user = Users( 
            username=user.username,
            email=user.email,
            first_name=user.first_name, 
            last_name=user.last_name, 
            password=get_password_hash(user.password),
        )

        
    try:
        # Add the new user to the database
        db.add(new_user) 
        db.commit()
        db.refresh(new_user) 
        
        # Claiming the refral 
        if(referrer):
            claim_new_refrral_by(referrer=referrer, 
                                 referred=new_user.id, 
                                 db=db)
            

        return JSONResponse(
            status_code=200,
            content= {
                "message": "User registered successfully.", 
                "username": new_user.username, 
            }
        )     
        
    except IntegrityError as e: 

        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists."
        )
        
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user. Error: {str(e)}"
        )


@router.post("/me", response_model=UserBase)
async def read_users_me(db: db_dependency, current_user: Users = Depends(get_current_user)): 
         
    return JSONResponse(
        status_code=200,
        content= {
            "username": current_user.username,
            "email": current_user.email, 
            "first_name": current_user.first_name, 
            "last_name": current_user.last_name,
            "is_email_verified": current_user.is_email_verified,  
        }
    )     