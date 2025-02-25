from pydantic import BaseModel
from ..services.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean
from ..utils.generate_refral import generate_referral

class Users(Base):
    __tablename__ = "users"
    
    username = Column(String(50), primary_key=True, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    referral_code = Column(String(10), unique=True, default=generate_referral())
    referred_by = Column(String(50), ForeignKey("users.username"), nullable=True)
    created_at = Column(DateTime, default=func.now()) 
    is_email_verified = Column(Boolean, default=False)  
