from pydantic import BaseModel
from typing import List, Optional

from Schemas.ObjectSchema import ObjectSchema

class ReservationSchema(BaseModel):
    userId : str
    deskId : str
    date:str
    startTime : str
    endTime : str
    anonymousBooking :Optional[bool]