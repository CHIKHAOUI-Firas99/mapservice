from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Schemas.Demands import DemandBase,DemandCreate,DemandUpdate
from Schemas.updateObjectMatTags import UpdateObjectSchema

from models.User import User
from models.Desk import Desk
from Controllers.DemandsController import delete_demand as delete,get_all_demands,get_demand,create_demand,update_demand as update,acceptDemand
from database.database import get_db

demandrouter = APIRouter()


@demandrouter.post("/demands/")
def add(demand: DemandCreate, desk_id: int, user_id: int, db: Session = Depends(get_db)):
    print('aaaaaaa')

    desk = db.query(Desk).filter(desk_id == desk_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_demand(db=db, demand=demand, desk_id=desk_id, user_id=user_id)


@demandrouter.get("/demands/")
def read_demands(db: Session = Depends(get_db)):
    demands = get_all_demands(db=db)
    return demands


@demandrouter.get("/demands/{demand_id}")
def read_demand(demand_id: int, db: Session = Depends(get_db)):
    db_demand = get_demand(db=db, demand_id=demand_id)
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return db_demand


@demandrouter.put("/demands/{demand_id}")
def update_demand(demand_id: int, demand: DemandUpdate, db: Session = Depends(get_db)):
    db_demand = get_demand(db=db, demand_id=demand_id)
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return update(db=db, demand_id=demand_id, demand=demand)


@demandrouter.delete("/demands/{demand_id}")
def delete_demand(demand_id: int, db: Session = Depends(get_db)):
    db_demand = get_demand(db=db, demand_id=demand_id)
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return delete(db=db, demand_id=demand_id)

@demandrouter.put("/acceptDemand/{desk_id}")
def update_demand(desk_id: int, equipements: UpdateObjectSchema, db: Session = Depends(get_db)):

    return acceptDemand(desk_id,equipements,db)