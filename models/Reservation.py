from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship


class Reservation(Base):
    __tablename__ = "reservations" 
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    desk_id = Column(Integer, ForeignKey('desks.desk_id'), primary_key=True)    
    start_time = Column(String(255))
    end_time = Column(String(255))
    date = Column(String(255))


    # Define the relationships between the association class and the other tables
    user = relationship("User", back_populates="desks")
    desk = relationship("Desk", back_populates="users")

