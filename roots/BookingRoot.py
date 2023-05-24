from fastapi import APIRouter, Depends
from Schemas.ReservationSchema import ReservationSchema
from models.User import User
from models.Desk import Desk
from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
from Controllers import BookingController





bookingRouter = APIRouter()



@bookingRouter.post("/reservation/")
async def makeReservation(request : ReservationSchema ,  db : Session = Depends(get_db)):
    return BookingController.makeReservation(request,db)


@bookingRouter.get("/get_available_time_slots/{desk_id}/{date}")
async def get_available_time_slots(desk_id,date ,db : Session = Depends(get_db)):
    return BookingController.get_available_time_slots(desk_id,date,db)

@bookingRouter.get("/reservationsPerDeskPerDay/{desk_id}/{date}")
async def getReservationsPerDeskPerDay(desk_id,date,db : Session = Depends(get_db)):
    return BookingController.getReservationsPerDeskPerDay(desk_id,date,db)
# get_user_reservations
@bookingRouter.get("/service2/getUserReservations/{user_id}")
async def getUserReservations(user_id,db : Session = Depends(get_db)):
    return BookingController.get_user_reservations(user_id,db)

@bookingRouter.get("/service2/getAllReservations/")
async def getUserReservations(db : Session = Depends(get_db)):
    return BookingController.get_all_reservations(db)

# cancelReservation
 
@bookingRouter.put("/service2/cancel-reservation/")
async def getUserReservations(request : ReservationSchema,db : Session = Depends(get_db)):
    return BookingController.cancelReservation(request,db)