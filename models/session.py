from pydantic import BaseModel
from ..services.database import Base
from sqlalchemy import Column, String

class SessionModel(Base):
    __tablename__ = "session"  
    sessionId = Column(String, primary_key=True, unique=True)
    title = Column(String)
    username = Column(String)
    body = Column(String)