from ctypes import py_object

from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId
import logging
from models import BuildingInput, BuildingResponse, Event, PyObjectId

logging.basicConfig(level=logging.INFO)  # Adjust the level if needed (e.g., DEBUG, WARNING, ERROR)
logger = logging.getLogger(__name__)
app = FastAPI()

# MongoDB connection
DB_USER = "db_user"
DB_PASSWORD = "ACoolPassword"
URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster.ism8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client: MongoClient = MongoClient(URI)
db = client['ikariam']

# Ping test endpoint
@app.get("/ping", response_model=str)
def ping():
    return "pong"

# Building endpoints
@app.post("/building/", response_model=BuildingResponse)
def create_building(building: BuildingInput):
    building_dict = building.dict()
    result = db['buildings'].insert_one(building_dict)
    building_dict["_id"] = result.inserted_id  # Store MongoDB's _id
    return building_dict

@app.get("/buildings", response_model=List[BuildingResponse])
def get_all_buildings():
    buildings = list(db['buildings'].find())
    return buildings

@app.get("/building", response_model=BuildingResponse)
def get_building(building_id: Optional[PyObjectId] = Query(None), building_name: Optional[str] = Query(None)):
    if not building_id and not building_name:
        raise HTTPException(status_code=400, detail="Either building id or building name must be provided.")
    query = {}
    if building_id:
        query["_id"] = ObjectId(building_id)
    if building_name:
        query["name"] = building_name

    # If both fields are provided, MongoDB will match only documents with both the specified ID and name.
    building = db['buildings'].find_one(query)
    logger.info(f"Query: {query}")

    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@app.put("/building", response_model=BuildingResponse)
def update_building_by_id(updated_building: BuildingInput, building_id: Optional[PyObjectId] = Query(None), building_name: Optional[str] = Query(None)):
    old_building = get_building(building_id, building_name)
    update_result = db['buildings'].update_one(
        {"_id": ObjectId(building_id)},
        {"$set": updated_building.dict()}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")
    return db['buildings'].find_one({"_id": ObjectId(building_id)})

@app.delete("/buildings/")
def delete_building(building_id: Optional[PyObjectId] = Query(None), building_name: Optional[str] = Query(None)):
    # Build query based on provided parameters
    query = {}
    if building_id:
        query["_id"] = ObjectId(building_id)
    if building_name:
        query["name"] = building_name
    delete_result = db['buildings'].delete_one(query)
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
