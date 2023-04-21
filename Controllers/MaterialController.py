import base64
from typing import List, Optional
from sqlalchemy.orm import Session
from Schemas.MaterialSchema import MaterialSchema

from models.Material import Material

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from PIL import UnidentifiedImageError
from fastapi import Form, HTTPException, UploadFile,File
from io import BytesIO
from PIL import Image, UnidentifiedImageError

from models.materialStock import MaterialStock
import base64
import io

from fastapi import HTTPException, status

async def create_material(
    db: Session,
    name: str = Form(...),
    picture: UploadFile = File(...),
    quantity: str = Form(...),
    # desk_id: str = Form(...)
):
    try:
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
            quantity=quantity
        )

        # Create a new material object using the ORM
        db_material = MaterialStock(
            name=material.name,
            picture=material.picture,
            quantity=material.quantity
        )

        # Add the material to the database
        db.add(db_material)
        db.commit()
        db.refresh(db_material)

        return {"message": "Material created successfully"}

    except (TypeError, ValueError, AttributeError, IOError, UnicodeDecodeError) as e:
        # handle the exception with HTTP status code 400 Bad Request
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except IntegrityError as e:
        # handle the database constraint violation with HTTP status code 409 Conflict
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="name already exists")

    except Exception as e:
        # handle any other unexpected exception with HTTP status code 500 Internal Server Error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the material")







async def get_material(db: Session, material_id: str) -> Material:
    material = db.query(MaterialStock).filter(MaterialStock.id == material_id).first()

    if not material:
        raise HTTPException(status_code=404, detail='Material not found')

    # Convert binary picture data to base64-encoded string
    material.picture = base64.b64encode(material.picture).decode('utf-8')

    return material











import base64
import asyncio
async def update_material(
    material_id: int,
    db: Session ,
    name: Optional[str] = Form(None),
    picture: Optional[UploadFile] = File(None),
    quantity: Optional[str] = Form(None),
    desk_id: Optional[str] = Form(None)
):
    # Get the material from the database
    db_material = db.query(MaterialStock).filter(MaterialStock.id == material_id).first()

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
        try:
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

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image"
            )

    try:
        db.commit()
        db.refresh(db_material)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name already exists"
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    return {"message": "Material updated successfully"}



def delete_material(db: Session, material_id: int) -> None:
    material = db.query(MaterialStock).filter(MaterialStock.id == material_id).first()
    if material:
        db.delete(material)
        db.commit()
     
    return {"detail": "Material deleted"}
import binascii

def get_all_materials(session: Session):
    materials = session.query(MaterialStock).all()
    decoded_materials = []
    material_names = set()
    
    for material in materials:
        if material.name not in material_names:
            decoded_material = material.__dict__
            if 'picture' in decoded_material:
                binary_data = material.picture
                base64_data = binascii.b2a_base64(binary_data).decode('utf-8')
                decoded_material['picture'] = base64_data
            decoded_materials.append(decoded_material)
            material_names.add(material.name)
    
    return decoded_materials
