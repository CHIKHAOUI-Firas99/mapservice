from pydantic import BaseModel
from typing import List , Union
from Schemas.ObjectSchema import ObjectSchema

from Schemas.ObjectUpdateSchema import ObjectUpdateSchema

class WorkspaceUpdateSchema(BaseModel):
    name : str
    mapUrl : str
    objects : List [Union[ObjectUpdateSchema,ObjectSchema]]
    tags :list=None