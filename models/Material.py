from sqlalchemy import BLOB, Column, ForeignKey, Integer, String,BINARY
from database.database import Base
from sqlalchemy import LargeBinary



class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    matname = Column(String(255))
    desk_id = Column(Integer, ForeignKey("desks.desk_id"))

    

