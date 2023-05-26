from sqlalchemy import BLOB, Column, ForeignKey, Integer, String,BINARY
from database.database import Base
from sqlalchemy import LargeBinary

from sqlalchemy.orm import relationship


class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    picture = Column(LargeBinary)
    quantity = Column(Integer)

    desk_materials = relationship("DeskMaterial", backref="materials", cascade='all, delete')
    

