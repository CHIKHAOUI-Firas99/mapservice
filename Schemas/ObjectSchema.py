from pydantic import BaseModel


class ObjectSchema(BaseModel):
    id:int
    path : str
    x : float
    y : float
    scaleX : float
    scaleY : float
    flipX : bool
    flipY : bool
    o : float
    type : str
    tags:list=None
    material:list=None
