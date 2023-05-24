from typing import List, Optional
from pydantic import BaseModel
from Schemas.MaterialSchema import MaterialSchema

class UpdateObjectSchema(BaseModel):
    material: Optional[list] 
    tags: Optional[list] 
