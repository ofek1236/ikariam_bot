from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pymongo import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId
from models import BuildingInput, BuildingResponse, Event

app = FastAPI()

# MongoDB connection
client: MongoClient = MongoClient('mongodb://db_user:ACoolPassword@atlas-sql-671c39d66bf5a9369fc49b15-3hllh.a.query.mongodb.net/ikariam?ssl=true&authSource=admin')
db = client['ikariam']

# Ping test endpoint
@app.get("/ping", response_model=str)
def ping():
    return "pong"

# Building endpoints
@app.post("/buildings/", response_model=BuildingResponse)
def create_building(building: BuildingInput):
    building_dict = building.dict()
    result = db['buildings'].insert_one(building_dict)
    building_dict["_id"] = result.inserted_id  # Store MongoDB's _id
    return building_dict

@app.get("/buildings/", response_model=List[BuildingResponse])
def get_all_buildings():
    buildings = list(db['buildings'].find())
    return buildings

@app.get("/buildings/{building_id}", response_model=BuildingResponse)
def get_building_by_id(building_id: str):
    building = db['buildings'].find_one({"_id": ObjectId(building_id)})
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@app.put("/buildings/{building_id}", response_model=BuildingResponse)
def update_building_by_id(building_id: str, updated_building: BuildingInput):
    update_result = db['buildings'].update_one(
        {"_id": ObjectId(building_id)},
        {"$set": updated_building.dict()}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")
    return db['buildings'].find_one({"_id": ObjectId(building_id)})

@app.delete("/buildings/{building_id}")
def delete_building_by_id(building_id: str):
    delete_result = db['buildings'].delete_one({"_id": ObjectId(building_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Building deleted successfully."}
    raise HTTPException(status_code=404, detail="Building not found")

# Event endpoints
@app.post("/events/", response_model=Event)
def create_event(event: Event):
    event_dict = event.dict()
    db['events'].insert_one(event_dict)
    return event

@app.get("/events/", response_model=List[Event])
def get_all_events():
    return list(db['events'].find())
