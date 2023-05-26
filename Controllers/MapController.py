from fastapi import HTTPException
from Helpers.ImageHelper import get_image_data, save_image_to_disk
from Schemas.WorkspaceSchema import WorkspaceSchema
from Schemas.WorkspaceUpdateSchema import WorkspaceUpdateSchema
from errors import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from models.Desk import Desk
from models.Door import Door
from models.DeskMaterial import DeskMaterial
from models.Object import Object
from models.Workspace import Workspace
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.Material import Material

def addWorkspace(request : WorkspaceSchema , db):
    workspace = Workspace(name = request.name , mapUrl = "",tags=request.tags)
    for o in request.objects:
        workspace.objects.append(createObject(o,[],db))
    try:
        workspace.mapUrl=save_image_to_disk(workspace.id,request.mapUrl)
        db.add(workspace)
        db.commit()
        return {"detail": "Workspace created successfully."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="name already in use")


def createObject(object, mat, db):
    print('create object function',mat)
    if object.type.upper() == "DESK":
        o = Desk(path=object.path,
                 x=object.x,
                 y=object.y,
                 scaleX=object.scaleX,
                 scaleY=object.scaleY,
                 flipX=object.flipX,
                 flipY=object.flipY,
                 o=object.o,
                 tags=object.tags
                 )
        db.add(o)  # add the object to the database
        db.flush()  # flush to get the ID of the object
        print('belllehyyyyyyy , ----->',o.id)
        print(mat)
        if mat:
            for material in mat:
                if material:
                    mat_in_stock = db.query(Material).filter(Material.name == material).first()
                    if mat_in_stock and mat_in_stock.quantity > 0:
                        mat_in_stock.quantity -= 1
                        db.add(DeskMaterial(material_id=mat_in_stock.id, desk_id=o.id))  # add the material to the database with the object ID
                        print('haaaaaaa')
                        print(mat)
                        db.commit()

                    # else:
                    #     db.rollback()
                        # raise HTTPException(status_code=404, detail="Material not found or out of stock")
            # commit the transaction to the database
        
    elif object.type.upper() == "DOOR":
        o = Door(path=object.path,
                 x=object.x,
                 y=object.y,
                 scaleX=object.scaleX,
                 scaleY=object.scaleY,
                 flipX=object.flipX,
                 flipY=object.flipY,
                 o=object.o,
                 tags=object.tags
                 )
    return o    






def getWorkspace(name: str, db: Session):
    workspace = db.query(Workspace).filter(Workspace.name == name).first()
    if workspace:
        listObjectNames = []
        if workspace.objects:
            for i in workspace.objects:
                if i.discriminator == 'desk':
                    desk_materials = db.query(DeskMaterial).filter(DeskMaterial.desk_id == i.id).all()
                    material_ids = [dm.material_id for dm in desk_materials]
                    values = []
                    for material_id in material_ids:
                        material = db.query(Material).filter(Material.id == material_id).first()
                        if material and material.name not in values:
                            values.append(material.name)
                    listObjectNames.append({'id': i.id, 'values': values})
        mapUrl = get_image_data(workspace.mapUrl)
        return {
            "id": workspace.id,
            "mapUrl": mapUrl,
            "name": workspace.name,
            "objects": workspace.objects,
            "tags": workspace.tags,
            "matnames": listObjectNames
        }
    else:
        return {}


def getWorkspacesNames(db):
    workspaces = db.query(Workspace).all()
    namesList = [w.name for w in workspaces]
    return namesList






def updateWorkspace(id: int, request: WorkspaceUpdateSchema, db: Session) -> None:
    """
    Update a workspace in the database.

    Args:
        name: The name of the workspace t o update.
        request: The new values for the workspace.
        db: The database session.

    Raises:
        HTTPException: If there is an error updating the workspace.
    """

    try:
        # Retrieve the workspace from the database.
        workspace = db.query(Workspace).filter(Workspace.id == id).first()
        # Update the workspace attributes.
        workspace.name = request.name
        workspace.mapUrl=save_image_to_disk(workspace.id,request.mapUrl)
        workspace.tags = request.tags

        # Keep track of the IDs of the objects that are currently in the workspace.
        current_object_ids = set(o.id for o in workspace.objects)
        new_object_ids=set(int(o.id) for o in request.objects)
        print(new_object_ids,'<---newwww')
        for item in current_object_ids:
            if item not in new_object_ids:
                print(item,'<--- item')
                desk_materials=db.query(DeskMaterial).filter(DeskMaterial.desk_id==item).all()
                mat=set()
                material_ids = [dm.material_id for dm in desk_materials]
                for item in material_ids:
                 material =db.query(Material).filter(Material.id == item).first()
                 material.quantity+=1   
                
                
                
                # for i in mat:
                #  matstock=db.query(Material).filter(Material.name==i).first()
                #  print('haaa')
                #  if matstock :
                #   matstock.quantity +=1
            # db.query(DeskMaterial).filter(DeskMaterial.desk_id==item).delete()
        # Update or create each object in the request.
        for obj_request in request.objects:

             
            obj_id = int(obj_request.id)
            if obj_id > 0:
                # Update an existing object.
                updateObject(obj_request, db)
                current_object_ids.remove(obj_id)

            else:
                print('ahwaaaaaaaa ------->',obj_request.material)
                # Create a new object.
                
                

                obj = createObject(obj_request,obj_request.material,db)
                workspace.objects.append(obj)
                print('object appeneded')

        # Delete any objects that are not in the request.
        for obj_id in current_object_ids:
            removeObject(obj_id, db)
        print('moshklt el committttttt')
        # Commit the changes to the database.
        db.commit()
        print('pffffffffff')
        allMatInstock=db.query(Material).all()
        for i in allMatInstock:
            if i.quantity == 0:
                matexist=db.query(DeskMaterial).filter(DeskMaterial.desk_id == i.id).first()

                if not matexist:
                   print('okkkkk1')
                   
                #    db.query(DeskMaterial).filter(DeskMaterial.desk_id == i.id).delete()
                   print('okkkkk2',i.id,db.query(Material).filter(Material.id == i.id).first().name)
                    
                #    matt=db.query(Material).filter(Material.id == i.id).first()
                #    db.delete(matt)
                   print('okkkkk3')

        db.commit()
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="name already exist")    

    except Exception as e:
        # Roll back the transaction and raise an HTTPException.
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def updateObject(o, db):
    print(o)
    obj = db.query(Object).filter(Object.id == o.id).first()
    obj.path = o.path
    obj.x = o.x
    obj.y = o.y
    obj.scaleX = o.scaleX
    obj.scaleY = o.scaleY
    obj.flipX = o.flipX
    obj.flipY = o.flipY
    obj.o = o.o
    obj.tags = o.tags
    existing_names=list()
    
    db_names = db.query(DeskMaterial).filter(DeskMaterial.desk_id == o.id).all()
    
    print(db_names,'desk id',o.id)
    for item in db_names:
      material_db= db.query(Material).filter(Material.id == item.material_id).first()
      if material_db:
        #  print(material_db.name)
         existing_names.append(material_db.name)
    print('torr')
    # db.query(DeskMaterial).filter(DeskMaterial.desk_id == o.id).delete()
    print('existing names ---> ',existing_names,'length existing ',len(db_names))
    new_mat_names = []
    if o.material:
        print('tttt')
        for material in o.material:
            new_mat_names.append(material)
            
            mat_in_stock = db.query(Material).filter(Material.name == material).first()
            if not mat_in_stock:
                print('not mat in stock')
                pass
                # raise HTTPException(status_code=404, detail="Material not found")

            elif material not in existing_names:
              if mat_in_stock :  
                if mat_in_stock.quantity > 0:
                  
                    mat_in_stock.quantity -= 1

                    mat = DeskMaterial(material_id=mat_in_stock.id,desk_id=o.id)
                    db.add(mat)

              
        for name in existing_names:
                    print('hana')
                    if name not in new_mat_names:
                     mat_stock = db.query(Material).filter(Material.name == name).first()
                     if mat_stock:
                      db.query(DeskMaterial).filter(DeskMaterial.material_id==mat_stock.id).delete()  
                      mat_stock.quantity += 1       

    
    
    else :
        for item in existing_names:
         mat=db.query(Material).filter(Material.name == item).first()
         if mat:
           
            mat.quantity+=1
            db.commit()
    db.commit()
    print('3')
    return {"message": "Object updated successfully"}


def removeObject(id,db):
    try:
        obj = db.query(Object).filter(Object.id == id).first()
        db.delete(obj)
        db.commit() 
        return {"detail": "Object deleted successfully."}
    except:
        raise HTTPException(status_code=500,detail="internal server error")
    

from sqlalchemy.orm import joinedload

def deleteWorkspace(workspace_id: int, db: Session):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    objects = db.query(Object).filter(Object.workspace_id == workspace_id).all()
    material_names = set()
    for obj in objects:
        if obj.discriminator == 'door':
          obj_id=obj.door_id
          print('dooor')
        else :
            obj_id = obj.desk_id
            print('desk')
        print(obj_id,'objjj id')
        materials = db.query(DeskMaterial).filter(DeskMaterial.desk_id == obj_id).all()
        print('hwwwww lmaterials',materials)
        for item in materials:
         print(item.desk_id)
         mat=db.query(Material).filter(Material.id ==item.material_id).first()
         if mat:
            print('ha233',mat.quantity)
            mat.quantity+=1
            db.commit()
            material_names.add(mat.name)  
            # db.delete(mat)      
     
        # for name in material_names:
        #     stock = db.query(Material).filter(Material.name == name).first()
        #     if stock:
        #         stock.quantity += 1
        # material_names.clear()
        db.delete(obj)

    db.delete(workspace)
    db.commit()
    return {"message": "Workspace deleted successfully"}


def update_object_tags_mat(object,name,action,db):
    print('rrr')
    workspace=db.query(Workspace).filter(Workspace.name==name).first()
    if workspace :
        print(action)
        if action == "create":
             print('waaaaaaa')
             k=createObject(object,object.material,db)
             workspace.objects.append(k) 
             db.commit()
             return k.id
        elif action =="update":
            print(object,'eeeeee')
            updateObject(object,db)
    else :         
        raise HTTPException(status_code=404,detail="desk should be affected inside a valid workspace")
 

    
      


