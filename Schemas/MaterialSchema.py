import base64
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, validator


class MaterialSchema(BaseModel):
    name: str = Form(...),
    picture: bytes 
    quantity: str = Form(...),
    desk_id: str = Form(...)
    
    # @validator('picture', pre=True)
    # def encode_picture(cls, v):
    #     # Convert binary picture data to base64-encoded string
    #     return base64.b64encode(v).decode('utf-8')
    
    @property
    def picture_url(self):
        # Computed property that returns the data URL for the base64-encoded picture data
        return f"data:image/jpeg;base64,{self.picture.decode('utf-8')}"
