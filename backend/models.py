from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId
from typing import Optional, List, Annotated

# Custom ObjectId type for Pydantic
PyObjectId = Annotated[str, BeforeValidator(str)]

class Event(BaseModel):
    name: str
    description: str
    start_level: int
    end_level: int

class BuildingInput(BaseModel):
    name: str
    level: int
    events: List[Event] = []

# Model with alias for response
class BuildingResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    level: int
    events: List[Event]

    class Config:
        allow_population_by_field_name = True  # Allow input by alias or original name
        json_encoders = {ObjectId: str}        # Encode ObjectId as a string in JSON
