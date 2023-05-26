from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Schemas.MaterialSchema import MaterialSchema
from Schemas.ObjectSchema import ObjectSchema
from Schemas.updateObjectMatTags import UpdateObjectSchema
from database.database import SessionLocal
from models.Material import DeskMaterial
from models.Object import Object
from models.Workspace import Workspace
from models.materialStock import MaterialStock



# CREATE function
def create_object(object: ObjectSchema, workspace_id: int, db: Session ):
    try:
        db_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not db_workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        db_object = Object(**object.dict(), workspace_id=workspace_id)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Object already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create object: {str(e)}")

# READ functions
def db_get_object(object_id: int, db: Session ):
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    return db_object
import binascii
def get_object_by_id(db: Session, object_id: int) -> ObjectSchema:
    db_object = db.query(Object).filter(Object.id == object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    
    # get the material affected to this object
    materials = db.query(DeskMaterial).filter(DeskMaterial.desk_id==object_id).all()
    listTags=db_object.tags
    result=list()
    d = {'materials': []}
    for item in materials:
     binary_data = item.picture
     base64_data = binascii.b2a_base64(binary_data).decode('utf-8')    
     d['materials'].append({'picture': base64_data, 'name': item.name})
     result.append(d)
    d.update({'tags':listTags})

    return d

def get_objects(workspace_id: int, db: Session ):
    db_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not db_workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return db_workspace.objects

# UPDATE function
def update_object(
    object_id: int, 
    updateObj:UpdateObjectSchema,
    db: Session
):
    db_object = db.query(Object).filter(Object.id == object_id).first()
    newnames=list()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
    db_names=db.query(DeskMaterial).filter(DeskMaterial.desk_id == object_id).all()
    existingnames=list()
    for item in db_names:
        print(item.name)
        
        existingnames.append(item.name)
    
    if updateObj.material:
          for item in updateObj.material:
              newnames.append(item.name)
            
    # Delete all materials associated with this object
    for item in existingnames:
        c= db.query(MaterialStock).filter(MaterialStock.name == item).first()
        if item not in newnames:
          c.quantity=c.quantity +1



        
    db.query(DeskMaterial).filter(DeskMaterial.desk_id == object_id).delete()

    # Create new materials for this object  
    
    if updateObj.material :
        for material in updateObj.material:


            material_data = DeskMaterial(
                name=material.name,
                picture=material.picture,
                quantity=material.quantity,
                desk_id=object_id
            )
            db.add(material_data)
            matInStock=db.query(MaterialStock).filter(MaterialStock.name == material.name).first()
            print(matInStock.quantity >0 and  matInStock.name not in existingnames )
            if matInStock.quantity >0 and  matInStock.name not in existingnames  :

                matInStock.quantity=matInStock.quantity-1
           
    if updateObj.tags:
        db_object.tags = updateObj.tags

    db.commit()
    if updateObj.material:
      
     if (matInStock.quantity == 0):
                db.query(MaterialStock).filter(MaterialStock.name == material.name).delete()
    # Update tags for this object
    db.commit()
    db.refresh(db_object)

    return {"message": "Object updated successfully"}


# DELETE function 
def delete_object(object_id: int, db: Session ):
    try:
        db_object = db.query(Object).filter(Object.id == object_id).first()
        if not db_object:
            raise HTTPException(status_code=404, detail="Object not found")
        db.delete(db_object)
        db.commit()
        return {"message": "Object deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete object: {str(e)}")

























def update_object(
    object_id: int, 
    update_obj: UpdateObjectSchema,
    db: Session
):
    db_object = db.query(Object).filter(Object.id == object_id).first()
    new_mat_names = []
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")
        
    db_names = db.query(DeskMaterial).filter(DeskMaterial.desk_id == object_id).all()
    existing_names = [item.name for item in db_names]
    
    if update_obj.material:
        for material in update_obj.material:
            new_mat_names.append(material)
            if material not in existing_names:
                mat_in_stock = db.query(MaterialStock).filter(MaterialStock.name == material).first()
                if mat_in_stock and mat_in_stock.quantity > 0:
                    mat_in_stock.quantity -= 1
                    db.add(DeskMaterial(
                        name=material,
                        picture=material.picture,
                        quantity=1,
                        desk_id=object_id
                    ))
                else:
                    db.rollback()
                    raise HTTPException(status_code=404, detail="Material not found or out of stock")

        for name in existing_names:
            if name not in new_mat_names:
                mat_stock = db.query(MaterialStock).filter(MaterialStock.name == name).first()
                if mat_stock:
                    mat_stock.quantity += 1

    if update_obj.tags:
        db_object.tags = update_obj.tags

    db.commit()

    db.refresh(db_object)

    return {"message": "Object updated successfully"}

