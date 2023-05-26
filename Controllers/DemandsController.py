from sqlalchemy.orm import Session
from models.Demandes import Demand
from Schemas.Demands import DemandCreate,DemandUpdate
from Controllers.MapController import updateObject
from datetime import datetime

from models.Material import DeskMaterial
from models.Notification import Notification
from models.materialStock import MaterialStock

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
            mat=db.query(MaterialStock).filter(MaterialStock.id==i.desk_id).first()
            if mat:
              
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
                mat=db.query(MaterialStock).filter(MaterialStock.id==i.desk_id).first()
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

import requests

def delete_demand(user_id:int,db: Session, demand_id: int):
    db_demand = db.query(Demand).filter(Demand.id == demand_id).first()
    print(demand_id,db_demand,'aaaaaaaaaaaa')
    # print(db_demand).status
    if db_demand:
        db_demand.status='refused'
        print('yoo')
        db.commit()
        # db.delete(db_demand)
        
        

        url = "http://localhost:8001/refuse_notifications/"+str(user_id)
        payload = {"des": "Unfortunately, we are unable to fulfill your material request at this time."}

        response = requests.post(url, json=payload)
        if response.status_code == 200:
         db.commit()
        else:
         print("Error: ", response.status_code)

        return True
    else:
        return False

from Controllers.ObjectController import update_object
def acceptDemand(user_id,desk_id,demandId,demand,equipements,db):
        new_mat_names=list()
        existing_names=[]
        db_names = db.query(DeskMaterial).filter(DeskMaterial.desk_id == desk_id).all()
        for item in db_names:
            mat = db.query(MaterialStock).filter(MaterialStock.id==item.desk_id).first()
            if mat:
              existing_names.append(mat.name)
        
        
        db.query(DeskMaterial).filter(DeskMaterial.desk_id == desk_id).delete()        
        print('my equipents ----->',equipements.material)
        for material in equipements.material:
            
            new_mat_names.append(material)
            print('mat appended')
            mat_in_stock = db.query(MaterialStock).filter(MaterialStock.name == material).first()
            if not mat_in_stock:
                print('not mat in stock')
                pass
                # raise HTTPException(status_code=404, detail="Material not found")

            elif material not in existing_names:
              if mat_in_stock :  
                mat_in_stock.quantity -= 1
            mat = DeskMaterial(material_id=mat_in_stock.id,desk_id=desk_id)
            db.add(mat)
            
            # if mat_in_stock:
              
            # #   if mat_in_stock.quantity == 0:
            # #     matexist=db.query(DeskMaterial).filter(DeskMaterial.name == material).first()
                # if not matexist:
                #   db.query(MaterialStock).filter(MaterialStock.name == material).delete()
              
        for name in existing_names:
                    
                    if name not in new_mat_names:
                     mat_stock = db.query(MaterialStock).filter(MaterialStock.name == name).first()
                     if mat_stock:
                      mat_stock.quantity += 1   
        print('saleeeeem')
        
        url = "http://localhost:8001/accept_notifications/"+str(user_id)
        payload = {"des": "Your material request has been accepted."}

        response = requests.post(url, json=payload)
        if response.status_code == 200:
         update_demand(db,demandId,demand)
         db.commit()
        else:
         print("Error: ", response.status_code)

        return 'OK' 



