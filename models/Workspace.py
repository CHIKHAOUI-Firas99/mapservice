from sqlalchemy import JSON, Column, Integer, String, LargeBinary, Text
from sqlalchemy.orm import relationship
from database.database import Base

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    tags = Column(JSON,nullable=True)
    mapUrl = Column(Text)
    objects = relationship("Object", back_populates="workspace", cascade='save-update')
    
