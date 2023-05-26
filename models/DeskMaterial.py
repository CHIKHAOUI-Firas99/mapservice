from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


# class Material(Base):
#     __tablename__ = "desk_materials"
#     material_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), primary_key=True)
#     desk_id = Column(Integer, ForeignKey("desks.desk_id"), primary_key=True, index=True)
#     desk = relationship("Desk", back_populates="materials")
#     # material = relationship("MaterialStock")
    
class DeskMaterial(Base):
    __tablename__ = "desk_materials"
    desk_id = Column(Integer, ForeignKey("desks.desk_id"), primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"), primary_key=True)