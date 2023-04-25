from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    matname = Column(String(255))
    desk_id = Column(Integer, ForeignKey("desks.desk_id"))
    desk = relationship("Desk", back_populates="materials")
    
