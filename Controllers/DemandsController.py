from sqlalchemy.orm import Session
from models.Demandes import Demand
from Schemas.Demands import DemandCreate,DemandUpdate
from Controllers.MapController import updateObject
from datetime import datetime

from models.DeskMaterial import DeskMaterial
from models.Notification import Notification
from models.Material import Material

def create_demand(db: Session, demand: DemandCreate, desk_id: int, user_id: int):

    demand_date = datetime.utcnow()

    db_demand = Demand(object=demand.object,description=demand.description, demandDate=demand_date,status='processing', desk_id=desk_id, user_id=user_id)
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand



def get_demand(db: Session, demand_id: int):
    demand= db.query(Demand).filter(Demand.id == demand_id).first()
    if demand:
        currentItemMaterials=db.query(DeskMaterial).filter(DeskMaterial.desk_id == demand.desk_id).all()
        print(currentItemMaterials)
        materialNames=set()
        for i in currentItemMaterials:
            mat=db.query(Material).filter(Material.id==i.material_id).first()
            if mat:
                print('aaa',mat.name)
                materialNames.add(mat.name)
         
        return {'description':demand.description,
                'object':demand.object,
                'equipements':materialNames,
                
                
                }


def get_all_demands(db: Session):
    allDemands = db.query(Demand).order_by(Demand.demandDate.desc()).all()
    l = []

    if allDemands:
        for item in allDemands:
            currentItemMaterials = db.query(DeskMaterial).filter(DeskMaterial.desk_id == item.desk_id).all()
            materialNames=set()
            for i in currentItemMaterials:
                mat=db.query(Material).filter(Material.id==i.material_id).first()
                if mat:
                  
                    materialNames.add(mat.name)
            d = {
                'id': item.id,
                'desk_id': item.desk_id,
                'user_id': item.user_id,
                'description': item.description,
                'object': item.object,
                'equipements': materialNames,
                'demandDate': item.demandDate,
                'status': item.status
            }
            l.append(d)

    # Sort the demands by status and demand date
    print('all demands',l)
    sortedDemands = sorted(l, key=lambda x: (x['status'] != 'processing', x['status'] != 'accepted'))
    print('sorted demand',sortedDemands)
    return sortedDemands




def update_demand(db: Session, demand_id: int, demand: DemandUpdate):
    db_demand = db.query(Demand).filter(Demand.id == demand_id).first()
    if db_demand:
        print(demand)
        if demand.status:
          db_demand.status=demand.status
        # db_demand.demandes = demand.demandes
        db.commit()
        db.refresh(db_demand)
        return db_demand
    else:
        return None

from sqlalchemy.orm import Session
import requests

def delete_demand(user_id: int, db: Session, demand_id: int):
    db_demand = db.query(Demand).filter(Demand.id == demand_id).first()
    print(demand_id, db_demand, 'aaaaaaaaaaaa')
    # print(db_demand).status
    if db_demand:
        db_demand.status = 'refused'
        print('yoo')
        db.commit()
        # db.delete(db_demand)
        with open('config.json', 'r') as file:
            config = json.load(file)

        url = config["NotificationServiceUrl"]+"/refuse_notifications/" + str(user_id)
        payload = {"des": "Unfortunately, we are unable to fulfill your material request."}

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            db.commit()
        else:
            print("Error:", response.status_code)

        return True
    else:
        return False


from Controllers.ObjectController import update_object
import json
import requests

def acceptDemand(user_id, desk_id, demandId, demand, equipements, db):
    # Read the config file
    with open('config.json', 'r') as file:
        config = json.load(file)

    new_mat_names = list()
    existing_names = set()
    db_names = db.query(DeskMaterial).filter(DeskMaterial.desk_id == desk_id).all()
    for item in db_names:
        mat = db.query(Material).filter(Material.id == item.material_id).first()
        if mat:
            existing_names.add(mat.name)

    # Rest of your code...

    url = config["NotificationServiceUrl"]+"/accept_notifications/"+str(user_id)  # Read the value from the config file
    payload = {"des": "Your material request has been accepted."}

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        update_demand(db, demandId, demand)
        db.commit()
    else:
        print("Error:", response.status_code)
    return 'OK'


