from sqlalchemy import Column, Integer
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index = True)
    user_id = Column(Integer , primary_key = True , index = True)
    desks = relationship("Reservation",back_populates="user")

