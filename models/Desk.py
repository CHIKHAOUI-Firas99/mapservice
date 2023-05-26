from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base
from models.Object import Object
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

class Desk(Object):
    __tablename__ = "desks"
    desk_id = Column(Integer, ForeignKey('objects.id'), primary_key=True)
    
    desk_materials = relationship("DeskMaterial", backref="desk", cascade='all, delete')
    users = relationship("Reservation", back_populates="desk")
    demandes = relationship("Demand", back_populates="desk")
    __mapper_args__ = dict(
        polymorphic_identity='desk'
    )

