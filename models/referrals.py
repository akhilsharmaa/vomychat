from pydantic import BaseModel
from ..services.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Enum
from enum import Enum as PyEnum
from sqlalchemy import UniqueConstraint

class ReferralStatus(PyEnum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    
class Refrrals(Base):
    __tablename__ = "refrrals"
    
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    referrer_user_id    = Column(String(50),  nullable=False)
    referred_user_id    = Column(String(50),  nullable=False)
    status              = Column(Enum(ReferralStatus), nullable=False, default=ReferralStatus.PENDING)
    date_referred       = Column(DateTime, default=func.now())
    