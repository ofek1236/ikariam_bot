from ctypes import py_object

from fastapi import FastAPI, HTTPException, Query, Body
from typing import List, Optional
from pymongo.mongo_client import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId
import logging
from models import BuildingInput, BuildingResponse, Event, PyObjectId, BuildingUpdate, Queue

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
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@app.put("/building", response_model=BuildingResponse)
def update_building(
        building_id: Optional[PyObjectId] = Query(None),
        building_name: Optional[str] = Query(None),
        updates: BuildingUpdate = Body(...)
):
    # Ensure that either an ID or name is provided
    if not building_id and not building_name:
        raise HTTPException(status_code=400,
                            detail="Either building_id or building_name must be provided to update a building.")

    # Build query to find the building
    query = {}
    if building_id:
        query["_id"] = ObjectId(building_id)
    if building_name:
        query["name"] = building_name

    # Prepare updates for MongoDB
    update_data = {k: v for k, v in updates.dict().items() if v is not None}  # Only include non-None fields
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    # Perform update operation
    update_result = db['buildings'].update_one(query, {"$set": update_data})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")

    # Fetch the updated document
    updated_building = db['buildings'].find_one(query)
    return updated_building


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


@app.post("/queues/", response_model=Queue)
def create_queue(queue: Queue):
    queue_dict = queue.dict()
    result = db['queues'].insert_one(queue_dict)
    queue_dict["_id"] = result.inserted_id  # Store MongoDB's _id
    return queue_dict

@app.get("/queues/", response_model=Queue)
def get_queue(username: str = Query(...)):
    queue = db['queues'].find_one({"username": username})
    if queue is None:
        raise HTTPException(status_code=404, detail="Queue not found")

    # Construct the Queue object to match the expected response model
    return queue

@app.delete("/queues/")
def delete_queue(username: str):
    # Build query based on provided parameters
    delete_result = db['queues'].delete_one({'username': username})
    if delete_result.deleted_count == 1:
        return {"message": "Queue deleted successfully."}
    raise HTTPException(status_code=404, detail="Queue not found")


# Event endpoints
@app.post("/events/", response_model=Queue)
def create_queue_event(queue_username: str, event: Event):
    new_event = event.dict()  # Convert Pydantic model to dictionary

    # Update query to add the new event to the user's queue array
    result = db['queues'].update_one(
        {"username": queue_username},           # Filter by the username
        {"$push": {"events": new_event}}    # Push the new event to the queue array
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User queue not found")

    # Optionally return the updated queue
    updated_queue = db['queues'].find_one({"username": queue_username})
    return updated_queue
