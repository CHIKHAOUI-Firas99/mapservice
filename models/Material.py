from sqlalchemy import BLOB, Column, ForeignKey, Integer, String,BINARY
from database.database import Base




class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer , primary_key = True , index = True)
    name = Column(String(255) , unique= True)
    picture=Column(BINARY)
    quantity=Column(Integer)
    desk_id = Column(Integer , ForeignKey("desks.desk_id"))

