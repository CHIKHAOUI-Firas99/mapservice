import base64
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, validator
from typing import Optional

class MaterialSchema(BaseModel):
    name: str 
    picture: Optional [bytes] 
    quantity: Optional[str] = None
    desk_id: Optional[str] = None
    description:Optional[str]=None

    
    # @validator('picture', pre=True)
    # def encode_picture(cls, v):
    #     # Convert binary picture data to base64-encoded string
    #     return base64.b64encode(v).decode('utf-8')
    
    @property
    def picture_url(self):
        # Computed property that returns the data URL for the base64-encoded picture data
        return f"data:image/jpeg;base64,{self.picture.decode('utf-8')}"
