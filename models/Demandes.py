from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class Demand(Base):
    __tablename__ = "demandes"
    id = Column(Integer, primary_key=True, index=True)
    demandes = Column(JSON, nullable=True)
    desk_id = Column(Integer, ForeignKey("desks.desk_id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    desk = relationship("Desk", back_populates="demandes")
    user = relationship("User", back_populates="demandes")
    demandDate=Column(DateTime)
   
