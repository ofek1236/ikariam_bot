# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Model for the building
class Building(BaseModel):
    id: int
    name: str
    level: int
    events: List[str]  # List of events related to the building

class Event(BaseModel):
    id: int
    building: Building
    level: int
    new_level: int

# In-memory database (for demonstration purposes)
buildings_db = []
events_db = []


@app.get("/ping", response_model=str)
def ping():
    return "pong"

@app.post("/buildings/", response_model=Building)
def create_building(building: Building):
    buildings_db.append(building)
    return building


@app.post("/events/", response_model=Building)
def create_event(event: Event):
    events_db.append(event)
    return event


@app.get("/buildings/", response_model=List[Building])
def read_buildings():
    return buildings_db

@app.get("/buildings/{building_id}", response_model=Building)
def read_building(building_id: int):
    for building in buildings_db:
        if building.id == building_id:
            return building
    return None  # Returns 404 if not found

@app.put("/buildings/{building_id}", response_model=Building)
def update_building(building_id: int, updated_building: Building):
    for index, building in enumerate(buildings_db):
        if building.id == building_id:
            buildings_db[index] = updated_building
            return updated_building
    return None  # Returns 404 if not found

@app.delete("/buildings/{building_id}")
def delete_building(building_id: int):
    for index, building in enumerate(buildings_db):
        if building.id == building_id:
            del buildings_db[index]
            return {"message": "Building deleted successfully."}
    return {"message": "Building not found."}
