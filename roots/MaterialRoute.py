import base64
import io
import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from Schemas.MaterialSchema import MaterialSchema
from database.database import get_db
from sqlalchemy.orm import Session
from database.database import get_db
from Controllers.MaterialController import create_material as addMat, get_material as getMat,get_all_materials, update_material as updateMat, delete_material
from models.Material import Material
from models.materialStock import MaterialStock


materialRouter = APIRouter()

logger = logging.getLogger(__name__)


from PIL import Image
# Dependency to get a database session

# Endpoint to create a new material
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from PIL import UnidentifiedImageError
# ...
@materialRouter.post("/materials")
async def create_material(db: Session = Depends(get_db),name: str = Form(...),picture: UploadFile = File(...),quantity: str = Form(...),):

    await addMat(db,name,picture,quantity)



@materialRouter.get("/materials/{material_id}")
async def get_material(material_id: int, db: Session = Depends(get_db)):


     return await getMat(db,material_id)

# Endpoint to update a material by ID
@materialRouter.put("/materials/{material_id}")
async def update_material(
    material_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    picture: Optional[UploadFile] = File(None),
    quantity: Optional[str] = Form(None),
    desk_id: Optional[str] = Form(None)
):
    # Get the material from the database
    await updateMat(material_id,db,name,picture,quantity,desk_id) 

    # Update the material in the database


# Endpoint to delete a material by ID
@materialRouter.delete("/materials/{material_id}")
async def delete_material_by_id(material_id: int, db: Session = Depends(get_db)):
    return delete_material(db,material_id)
@materialRouter.get("/materials")
async def getAllMaterials( db: Session = Depends(get_db)):
    
    return get_all_materials(db)