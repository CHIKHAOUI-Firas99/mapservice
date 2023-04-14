from fastapi import HTTPException
from Schemas.WorkspaceSchema import WorkspaceSchema
from Schemas.WorkspaceUpdateSchema import WorkspaceUpdateSchema
from errors import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from models.Desk import Desk
from models.Door import Door
from models.Object import Object
from models.Workspace import Workspace
from sqlalchemy.exc import IntegrityError

def addWorkspace(request : WorkspaceSchema , db):
    workspace = Workspace(name = request.name , mapUrl = request.mapUrl,tags=request.tags)
    for o in request.objects:
        workspace.objects.append(createObject(o))
    try:
        db.add(workspace)
        db.commit()
        return {"detail": "Workspace created successfully."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="name already in use")


def createObject(object):
    if(object.type.upper() == "DESK"):
        o =  Desk(path = object.path,
                    x = object.x,
                    y = object.y,
                    scaleX = object.scaleX,
                    scaleY = object.scaleY,
                    flipX = object.flipX,
                    flipY = object.flipY,
                    o = object.o,
                    tags=object.tags
                    )
        return o
    elif (object.type.upper() == "DOOR"):
        o = Door(path = object.path,
                    x = object.x,
                    y = object.y,
                    scaleX = object.scaleX,
                    scaleY = object.scaleY,
                    flipX = object.flipX,
                    flipY = object.flipY,
                    o = object.o,
                    tags=object.tags
                    )
        return o





def getWorkspace(name : str,db):
    workspace = db.query(Workspace).filter(Workspace.name == name).first()
    if(workspace):
        return {
        "id":workspace.id,
        "mapUrl":workspace.mapUrl,
        "name" : workspace.name,
        "objects":workspace.objects,
        "tags":workspace.tags
    }
    else:
        return {}

def getWorkspacesNames(db):
    workspaces = db.query(Workspace).all()
    namesList = [w.name for w in workspaces]
    return namesList

from sqlalchemy.orm import Session
def updateWorkspace(id: int, request: WorkspaceUpdateSchema, db: Session) -> None:
    """
    Update a workspace in the database.

    Args:
        name: The name of the workspace to update.
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
        workspace.mapUrl = request.mapUrl
        workspace.tags = request.tags

        # Keep track of the IDs of the objects that are currently in the workspace.
        current_object_ids = set(o.id for o in workspace.objects)

        # Update or create each object in the request.
        for obj_request in request.objects:
            obj_id = obj_request.id

            if obj_id > 0:
                # Update an existing object.
                updateObject(obj_request, db)
                current_object_ids.remove(obj_id)
            else:
                # Create a new object.
                obj = createObject(obj_request)
                workspace.objects.append(obj)

        # Delete any objects that are not in the request.
        for obj_id in current_object_ids:
            removeObject(obj_id, db)

        # Commit the changes to the database.
        db.commit()
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="name already exist")    

    except Exception as e:
        # Roll back the transaction and raise an HTTPException.
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def updateObject(o,db):
    obj = db.query(Object).filter(Object.id == o.id).first()
    obj.path = o.path
    obj.x = o.x
    obj.y = o.y
    obj.scaleX = o.scaleX
    obj.scaleY = o.scaleY
    obj.flipX = o.flipX
    obj.flipY = o.flipY
    obj.o = o.o
    db.commit()

def removeObject(id,db):
    try:
        obj = db.query(Object).filter(Object.id == id).first()
        db.delete(obj)
        db.commit() 
        return {"detail": "Object deleted successfully."}
    except:
        raise HTTPException(status_code=500,detail="internal server error")
    

def deleteWorkspace(workspace_id: int, db: Session) -> None:
    """
    Delete a workspace from the database.

    Args:
        workspace_id: The ID of the workspace to delete.
        db: The database session.
    """

    try:
        # Retrieve the workspace from the database.
        workspace = db.query(Workspace).get(workspace_id)

        if workspace:
            # Delete the workspace and commit the transaction.
            db.delete(workspace)
            db.commit()
            return {"detail":"delete succedded"}
        else:
            # The workspace was not found in the database.
            raise HTTPException(status_code=404, detail="Workspace not found")

    except Exception as e:
        # Roll back the transaction and raise an HTTPException.
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

