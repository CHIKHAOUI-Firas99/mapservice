from sqlalchemy import JSON, TEXT, Column, DateTime, ForeignKey, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class Demand(Base):
    __tablename__ = "demands"
    id = Column(Integer, primary_key=True, index=True)
    object =Column(String(255))
    description=status=Column(TEXT)
    # demandes = Column(JSON, nullable=True)
    status=Column(String(255))
    desk_id = Column(Integer, ForeignKey("desks.desk_id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    desk = relationship("Desk", back_populates="demandes")
    user = relationship("User", back_populates="demandes")
    demandDate=Column(DateTime)
   
