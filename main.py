from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base,engine
from models.Desk import Desk
from models.User import User
from models.Workspace import Workspace
from models.Reservation import Reservation
from models.Door import Door
from models.Material import Material
from models.DeskMaterial import DeskMaterial

from models.Demandes import Demand
from models.Notification import Notification
from models.Role import Role


from roots.MapRoot import mapRouter
from roots.MaterialRoute import materialRouter
from roots.demandsRoot import demandrouter
from roots.NotificationRoute import notificationRouter
from sqlalchemy.orm import Session
from database.database import get_db
from roots.ObjectRoot import ObjectRouter
from roots.BookingRoot import bookingRouter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
@app.get("/")
async def root(db : Session = Depends(get_db)):
 return db.query(User).filter(User.id == 1).first()


app.include_router(mapRouter)
app.include_router(materialRouter)
app.include_router(ObjectRouter)
app.include_router(demandrouter)
app.include_router(notificationRouter)

# bookingRouter
app.include_router(bookingRouter)