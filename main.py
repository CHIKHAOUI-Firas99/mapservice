from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base,engine
from models.Desk import Desk
from models.User import User
from models.Workspace import Workspace
from models.Reservation import Reservation
from models.Door import Door
from models.Material import Material
from roots.MapRoot import mapRouter
from roots.MaterialRoute import materialRouter
from sqlalchemy.orm import Session
from database.database import get_db

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
    desk = Desk(path = "aa" , aaa = "aaaaaa")
    db.add(desk)
    db.commit()

app.include_router(mapRouter)
app.include_router(materialRouter)