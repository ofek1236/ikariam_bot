from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId
from typing import Optional, List, Annotated

# Custom ObjectId type for Pydantic
PyObjectId = Annotated[str, BeforeValidator(str)]

class Event(BaseModel):
    building_name: str
    start_level: int
    end_level: int

class Queue(BaseModel):
    username: str
    events: Optional[List[Event]] = []


class BuildingInput(BaseModel):
    name: str
    level: int
    wood: Optional[int]
    marbel: Optional[int]
    sulphur: Optional[int]
    crystal: Optional[int]
    # events: List[Event] = []

class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    wood: Optional[int] = None
    marbel: Optional[int] = None
    sulphur: Optional[int] = None
    crystal: Optional[int] = None
    # events: Optional[List[Event]] = None

# Model with alias for response
class BuildingResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    level: int
    wood: Optional[int] = 0
    marbel: Optional[int] = 0
    sulphur: Optional[int] = 0
    crystal: Optional[int] = 0

    class Config:
        allow_population_by_field_name = True  # Allow input by alias or original name
        json_encoders = {ObjectId: str}        # Encode ObjectId as a string in JSON
