from typing import List, Dict, Any, Optional
from pydantic import BaseModel, validator



class DemandBase(BaseModel):
    object:str
    description: Optional[str]
    status: Optional[str]




class DemandCreate(DemandBase):
    pass


class DemandUpdate(DemandBase):
    pass
