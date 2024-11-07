from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, Dict, List


class Event(BaseModel):
    building_name: str
    level: int


class BuildingInput(BaseModel):
    name: str
    level: int
    wood: Optional[int]
    marbel: Optional[int]
    sulphur: Optional[int]
    crystal: Optional[int]


class BuildingResponse(BaseModel):
    name: str
    level: int
    wood: Optional[int] = 0
    marble: Optional[int] = 0
    sulphur: Optional[int] = 0
    crystal: Optional[int] = 0

    class Config:
        allow_population_by_field_name = True  # Allow input by alias or original name
        json_encoders = {ObjectId: str}  # Encode ObjectId as a string in JSON


class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    wood: Optional[int] = None
    marbel: Optional[int] = None
    sulphur: Optional[int] = None
    crystal: Optional[int] = None


class Queue(BaseModel):
    username: str
    events: Dict[str, Optional[List[BuildingResponse]]] = {}
