import base64
import io
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from Controllers.ObjectController import get_object_by_id,update_object
from Schemas.MaterialSchema import MaterialSchema
from Schemas.ObjectSchema import ObjectSchema
from Schemas.updateObjectMatTags import UpdateObjectSchema
from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
ObjectRouter = APIRouter()
@ObjectRouter.get("/object/{id}")
async def getObject(id:int ,db: Session = Depends(get_db)):
    
    return get_object_by_id(db,id)

@ObjectRouter.put("/object/{id}")
async def getObject(id: int, u:UpdateObjectSchema, db: Session = Depends(get_db)):
    print('aaaaa')
    return update_object(id, u, db)


