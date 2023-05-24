from fastapi import APIRouter,Depends,status
from Schemas.WorkspaceSchema import WorkspaceSchema
from Schemas.WorkspaceUpdateSchema import WorkspaceUpdateSchema

from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
from Controllers import MapController,BookingController



mapRouter = APIRouter()

@mapRouter.post('/workspace',status_code=status.HTTP_201_CREATED)
async def addWorkspace(request : WorkspaceSchema , db : Session = Depends(get_db)):
    return MapController.addWorkspace(request,db)

@mapRouter.get('/workspace')
async def getWorkspace(name :str, db : Session = Depends(get_db)):
    return MapController.getWorkspace(name,db)

@mapRouter.get('/workspaces_names')
async def getWorkspacesNames(db : Session = Depends(get_db)):
    return MapController.getWorkspacesNames(db)

@mapRouter.put('/workspace/{id}')
async def updateWorkspace(id : str, request : WorkspaceUpdateSchema, db : Session = Depends(get_db)):
    return  MapController.updateWorkspace(id,request,db)

@mapRouter.delete('/object/{id}')
async def removeObject(id,db : Session = Depends(get_db)):
    return MapController.removeObject(id,db)

@mapRouter.delete('/workspace/{id}')
async def removeObject(id,db : Session = Depends(get_db)):
    return MapController.deleteWorkspace(id,db)



@mapRouter.get('/workspaces')
async def getWorkspacesForBooking(date :str,userId,db : Session = Depends(get_db)):
    return BookingController.getWorkspacesForBooking(date,userId,db)


@mapRouter.get('/workspaceToBook')
async def getWorkspaceForBook(date :str,userId,name:str,db : Session = Depends(get_db)):
    return BookingController.getWorkspaceForBook(date,userId,name,db)