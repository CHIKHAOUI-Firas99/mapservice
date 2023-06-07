from fastapi import APIRouter, Depends
from Schemas.ReservationSchema import ReservationSchema
from models.User import User
from models.Desk import Desk
from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
from Controllers import BookingController





bookingRouter = APIRouter()



@bookingRouter.post("/mapService/reservation/")
async def makeReservation(request : ReservationSchema ,  db : Session = Depends(get_db)):
    return BookingController.makeReservation(request,db)


@bookingRouter.get("/mapService/get_available_time_slots/{desk_id}/{date}")
async def get_available_time_slots(desk_id,date ,db : Session = Depends(get_db)):
    return BookingController.get_available_time_slots(desk_id,date,db)

@bookingRouter.get("/mapService/reservationsPerDeskPerDay/{desk_id}/{date}")
async def getReservationsPerDeskPerDay(desk_id,date,db : Session = Depends(get_db)):
    return BookingController.getReservationsPerDeskPerDay(desk_id,date,db)
# get_user_reservations
@bookingRouter.get("/mapService/getUserReservations/{user_id}")
async def getUserReservations(user_id,db : Session = Depends(get_db)):
    return BookingController.get_user_reservations(user_id,db)

@bookingRouter.get("/mapService/getAllReservations/")
async def getUserReservations(db : Session = Depends(get_db)):
    return BookingController.get_all_reservations(db)

# cancelReservation
 
@bookingRouter.put("/mapService/cancel-reservation/")
async def getUserReservations(request : ReservationSchema,db : Session = Depends(get_db)):
    return BookingController.cancelReservation(request,db)