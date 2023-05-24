from sqlalchemy import BLOB, Column, ForeignKey, Integer, String,BINARY
from database.database import Base
from sqlalchemy import LargeBinary




class MaterialStock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),unique=True)
    picture = Column(LargeBinary)
    quantity = Column(Integer)

    

