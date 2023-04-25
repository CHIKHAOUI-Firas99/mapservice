from typing import List, Dict, Any
from pydantic import BaseModel, validator
class DemandMaterial(BaseModel):
    material: str
    quantity: int


class DemandBase(BaseModel):
    demandes: list[DemandMaterial]




class DemandCreate(DemandBase):
    pass


class DemandUpdate(DemandBase):
    pass
