from fastapi import APIRouter,Depends,status
from Schemas.ObjectSchema import ObjectSchema
from Schemas.WorkspaceSchema import WorkspaceSchema
from Schemas.WorkspaceUpdateSchema import WorkspaceUpdateSchema

from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
from Controllers import MapController,BookingController



mapRouter = APIRouter()

@mapRouter.post('/mapService/workspace',status_code=status.HTTP_201_CREATED)
async def addWorkspace(request : WorkspaceSchema , db : Session = Depends(get_db)):
    return MapController.addWorkspace(request,db)

@mapRouter.get('/mapService/workspace')
async def getWorkspace(name :str, db : Session = Depends(get_db)):
    return MapController.getWorkspace(name,db)

@mapRouter.get('/mapService/workspaces_names')
async def getWorkspacesNames(db : Session = Depends(get_db)):
    return MapController.getWorkspacesNames(db)

@mapRouter.put('/mapService/workspace/{id}')
async def updateWorkspace(id : str, request : WorkspaceUpdateSchema, db : Session = Depends(get_db)):
    return  MapController.updateWorkspace(id,request,db)

@mapRouter.delete('/mapService/object/{id}')
async def removeObject(id,db : Session = Depends(get_db)):
    return MapController.removeObject(id,db)

@mapRouter.delete('/mapService/workspace/{id}')
async def removeObject(id,db : Session = Depends(get_db)):
    return MapController.deleteWorkspace(id,db)
# getDeskMatTags
@mapRouter.get('/mapService/getDeskMatTags/{desk_id}')
async def removeObject(desk_id,db : Session = Depends(get_db)):
    return MapController.getDeskMatTags(desk_id,db)

@mapRouter.get('/mapService/workspaces')
async def getWorkspacesForBooking(date :str,userId,db : Session = Depends(get_db)):
    return BookingController.getWorkspacesForBooking(date,userId,db)


@mapRouter.get('/mapService/workspaceToBook')
async def getWorkspaceForBook(date :str,userId,name:str,db : Session = Depends(get_db)):
    return BookingController.getWorkspaceForBook(date,userId,name,db)

@mapRouter.put('/mapService/update_desk/{name}')
async def updateDeskDetails(object:ObjectSchema,name:str,action,db : Session = Depends(get_db)):    
    return MapController.update_object_tags_mat(object,name,action,db)