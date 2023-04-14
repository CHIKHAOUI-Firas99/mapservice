import base64
from typing import List
from sqlalchemy.orm import Session
from Schemas.MaterialSchema import MaterialSchema

from models.Material import Material


from fastapi import Form, HTTPException, UploadFile,File
from io import BytesIO
from PIL import Image


async def create_material(
    db: Session ,
    name: str = Form(...),
    picture: UploadFile = File(...),
    quantity: str = Form(...),
    desk_id: str = Form(...)
):
    # Read the contents of the uploaded file as bytes
    picture_data = await picture.read()

    # Convert binary picture data to base64-encoded string
    encoded_picture_data = base64.b64encode(picture_data).decode('utf-8')

    material = MaterialSchema(
        name=name,
        picture=encoded_picture_data,
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



def get_material(db: Session, material_id: str) -> Material:
    material= db.query(Material).filter(Material.id == material_id).first()
    if material:
            print(material.picture)
            image_data = base64.b64decode(material.picture.decode('utf-8').strip().split(',', 1)[1].encode('utf-8'))




            # Update the material dictionary to include the image data as a string
            material_with_image = material.copy()
            material_with_image['picture'] = image_data.decode('utf-8')
            return material_with_image
    return material_with_image

import base64
import asyncio

async def update_material(db: Session, material_id: int, material: MaterialSchema):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    print(material)
    if material['name']:
        db_material.name = material['name']
    
    if material['picture']:
        print('3os')
        # Read the contents of the uploaded file as bytes
        pic = await material['picture'].read()
        print('ahla')
        # Convert binary picture data to base64-encoded string
        pic_bytes = await pic
        print('hi')
        encoded_picture_data = base64.b64encode(pic_bytes).decode('utf-8')
        print('hello')
        db_material.picture = encoded_picture_data
    
    if material['quantity']:
        db_material.quantity = material['quantity']
    
    if material['desk_id']:
        db_material.desk_id = material.desk_id
    
    db.commit()
    db.refresh(db_material)
    
    return {"message": "Material updated successfully"}




def delete_material(db: Session, material_id: int) -> None:
    material = db.query(Material).filter(Material.id == material_id).first()
    if material:
        db.delete(material)
        db.commit()
import binascii

def get_all_materials(session: Session):
    materials = session.query(Material).all()
    decoded_materials = []
    
    for material in materials:
        decoded_material = material.__dict__
        if 'picture' in decoded_material:
            binary_data = material.picture
            base64_data = binascii.b2a_base64(binary_data).decode('utf-8')
            decoded_material['picture'] = base64_data
        decoded_materials.append(decoded_material)
    
    return decoded_materials