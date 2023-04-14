from pydantic import BaseModel
from typing import List

from Schemas.ObjectSchema import ObjectSchema

class WorkspaceSchema(BaseModel):
    name : str
    mapUrl : str
    tags:list=None
    objects : List[ObjectSchema]
