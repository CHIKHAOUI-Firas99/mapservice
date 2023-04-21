from pydantic import BaseModel


class ObjectUpdateSchema(BaseModel):
    id:str
    path : str
    x : float
    y : float
    scaleX : float
    scaleY : float
    flipX : bool
    flipY : bool
    o : float
    type : str
    tags:list
    material:list=None