from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, constr
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from ..services.database import db_dependency
from ..models.users import Users
from ..utils.passwords import get_password_hash
from ..utils.users import get_current_user
from fastapi.responses import JSONResponse
from ..services.claim_refrral import claim_new_refrral_by

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
) 


class UserBase(BaseModel): 
    username: constr(min_length=3, max_length=50) = Field(..., description="Username must be between 3 and 50 characters.")
    email: EmailStr = Field(..., description="Valid email address.")
    first_name: constr(min_length=1, max_length=50) = Field(..., description="First name must be between 1 and 50 characters.")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="Last name must be between 1 and 50 characters.")
    password: constr(min_length=8) = Field(..., description="Password must be at least 8 characters.")


@router.post("/register")
async def create_user(user: UserBase, db: db_dependency, referrer: Optional[str] = Query(None, description="Referrer username")):

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
        if referrer:
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
            detail="A user with this email or username already exists."
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