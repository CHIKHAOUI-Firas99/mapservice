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
from Controllers.MaterialController import create_material, get_material,get_all_materials, update_material, delete_material
from models.Material import Material


materialRouter = APIRouter()

logger = logging.getLogger(__name__)


from PIL import Image
# Dependency to get a database session

# Endpoint to create a new material
@materialRouter.post("/materials")



async def create_material(
    db: Session = Depends(get_db),
    name: str = Form(...),
    picture: UploadFile = File(...),
    quantity: str = Form(...),
    desk_id: str = Form(...)
):
    # Read the image file content
    image_content = await picture.read()

    # Resize the image and convert it to JPEG format
    image = Image.open(io.BytesIO(image_content))
    image = image.convert("RGB")
    image = image.resize((300, 300))
    with io.BytesIO() as buffer:
        image.save(buffer, "JPEG")
        image_data = buffer.getvalue()

    # Encode the image content in base64
    image_str = base64.b64encode(image_data).decode("utf-8")

    material = MaterialSchema(
        name=name,
        picture=image_str,
        quantity=quantity,
        desk_id=desk_id
    )

    # Create a new material object using the ORM
    db_material = Material(
        name=material.name,
        picture=material.picture,
        quantity=material.quantity,
        desk_id=material.desk_id
    )

    # Add the material to the database
    db.add(db_material)
    db.commit()
    db.refresh(db_material)

    return {"message": "Material created successfully"}


# Endpoint to get a material by ID
@materialRouter.get('/materials/{material_id}')
async def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()

    if not material:
        raise HTTPException(status_code=404, detail='Material not found')

    # Convert binary picture data to base64-encoded string
    material.picture = base64.b64encode(material.picture).decode('utf-8')

    return material

# Endpoint to update a material by ID
@materialRouter.put("/materials/{material_id}")
async def update_material(
    material_id:int,
    db: Session = Depends(get_db),
    
    name: Optional[str] = Form(None),
    picture: Optional[UploadFile] = File(None),
    quantity: Optional[str] = Form(None),
    desk_id: Optional[str] = Form(None)
):
    # Get the material from the database
    db_material = db.query(Material).filter(Material.id == material_id).first()

    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Update the material fields if they are provided
    if name:
        db_material.name = name
    if quantity:
        db_material.quantity = quantity
    if desk_id:
        db_material.desk_id = desk_id
    if picture:
        # Read the image file content
        image_content = await picture.read()

        # Open the image using Pillow
        image = Image.open(io.BytesIO(image_content))

        # Resize the image
        image = image.resize((500, 500))

        # Convert the image to RGB mode
        image = image.convert("RGB")

        # Save the image to a byte stream
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='JPEG')

        # Encode the image content in base64
        image_data = base64.b64encode(image_byte_array.getvalue())

        # Decode the base64 string to a regular string
        image_str = image_data.decode('utf-8')

        db_material.picture = image_str.encode('utf-8')

    # Update the material in the database
    db.commit()
    db.refresh(db_material)

    return {"message": "Material updated successfully"}
# Endpoint to delete a material by ID
@materialRouter.delete("/materials/{material_id}")
async def delete_material_by_id(material_id: int, db: Session = Depends(get_db)):
    delete_material(db, material_id)
    return {"detail": "Material deleted"}
@materialRouter.get("/materials")
async def getAllMaterials( db: Session = Depends(get_db)):
    return get_all_materials(db)