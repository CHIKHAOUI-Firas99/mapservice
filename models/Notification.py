from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from database.database import Base
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    
   
