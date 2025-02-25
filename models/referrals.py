from pydantic import BaseModel
from ..services.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from ..utils.generate_refral import generate_referral
from enum import Enum 

class ReferralStatus(Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    
    
class Refrrals(Base):
    
    __tablename__ = "refrrals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    refrral_code = Column(String(6), nullable=False)
    referrer_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    referred_user_id = Column(String(50), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(ReferralStatus), nullable=False, 
                    default=ReferralStatus.PENDING)
    date_referred = Column(DateTime, default=func.now()) 
    
    # Relationship
    referrer = relationship("User", foreign_keys=[referrer_id])
    referred_user = relationship("User", foreign_keys=[referred_user_id])