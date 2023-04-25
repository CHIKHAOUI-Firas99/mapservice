from sqlalchemy.orm import Session
from models.Demandes import Demand
from Schemas.Demands import DemandCreate,DemandUpdate

from datetime import datetime

from models.Material import Material

def create_demand(db: Session, demand: DemandCreate, desk_id: int, user_id: int):
    demand_dict = [{"material": dm.material, "quantity": dm.quantity} for dm in demand.demandes]
    demand_date = datetime.utcnow()

    db_demand = Demand(demandes=demand_dict, demandDate=demand_date, desk_id=desk_id, user_id=user_id)
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand



def get_demand(db: Session, demand_id: int):
    return db.query(Demand).filter(Demand.id == demand_id).first()


def get_all_demands(db: Session):
    allDemnds= db.query(Demand).all()
    l=list()
    for item in allDemnds:
       
        currentItemMaterials=db.query(Material).filter(Material.desk_id == item.desk_id).all()
        materialNames=set(o.matname for o in currentItemMaterials)
        d=dict()
        d.update({
            'desk_id':item.desk_id,
            'user_id':item.user_id,
            'demands':item.demandes,
            'equipements':materialNames,
            'demandDate':item.demandDate

        })
        l.append(d)
    return l 


def update_demand(db: Session, demand_id: int, demand: DemandUpdate):
    db_demand = db.query(Demand).filter(Demand.id == demand_id).first()
    if db_demand:
        print(demand)
        
        demand_dict = [{"material": dm.material, "quantity": dm.quantity} for dm in demand.demandes]
        db_demand.demandes = demand_dict
        
        db.commit()
        db.refresh(db_demand)
        return db_demand
    else:
        return None



def delete_demand(db: Session, demand_id: int):
    db_demand = db.query(Demand).filter(Demand.id == demand_id).first()
    if db_demand:
        db.delete(db_demand)
        db.commit()
        return True
    else:
        return False

from Controllers.ObjectController import update_object
def acceptDemand(desk_id,equipements,db):
    return update_object(desk_id,equipements,db)

