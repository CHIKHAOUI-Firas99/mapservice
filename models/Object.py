from sqlalchemy import  Column, ForeignKey, Integer,Float, String,Boolean
from database.database import Base 
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship

class Object(Base):
    
    __tablename__ = "objects"
    id = Column(Integer , primary_key = True , index = True)
    path = Column(String(255))
    x = Column(Float)
    y = Column(Float)
    scaleX = Column(Float)
    scaleY = Column(Float)
    flipX = Column(Boolean)
    flipY = Column(Boolean)
    o = Column(Float) 
    

    tags = Column(JSON,nullable=True)
    discriminator = Column('type', String(50))

    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    workspace = relationship("Workspace", back_populates="objects")
    __mapper_args__ = {
        'polymorphic_on': discriminator,
        'polymorphic_identity': 'object'
        
    }
