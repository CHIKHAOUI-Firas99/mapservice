from sqlalchemy import Column, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index = True)
    name=Column(String(250))
    demandes = relationship("Demand", uselist=False, back_populates="user", cascade="all, delete-orphan")
    desks = relationship("Reservation", back_populates="user")

