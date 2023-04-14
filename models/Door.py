from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base
from models.Object import Object


class Door(Object):
    __tablename__ = "doors"
    door_id = Column(Integer, ForeignKey('objects.id'), primary_key=True)
    aaa = Column(String(250))
    __mapper_args__ = dict(
        polymorphic_identity = 'door'
    
    )
