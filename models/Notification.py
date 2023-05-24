from sqlalchemy import BOOLEAN, JSON, Column, DateTime, ForeignKey, Integer, String, Text
from database.database import Base
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    time=Column(DateTime)
    read=Column(BOOLEAN)
    title=Column(String(100))
    level=Column(String(10),nullable=True)

    
   
