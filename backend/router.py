from fastapi import FastAPI, HTTPException, Query
from pymongo.mongo_client import MongoClient
import logging
from models import Queue, Event
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(
    level=logging.INFO
)  # Adjust the level if needed (e.g., DEBUG, WARNING, ERROR)
logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
DB_USER = "db_user"
DB_PASSWORD = "ACoolPassword"
URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster.ism8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
client: MongoClient = MongoClient(URI)
db = client["ikariam"]


# Ping test endpoint
@app.get("/ping", response_model=str)
def ping():
    return "pong"


@app.post("/queues/", response_model=Queue)
def create_queue(queue: Queue):
    queue_dict = queue.dict()
    result = db["queues"].insert_one(queue_dict)
    queue_dict["_id"] = result.inserted_id  # Store MongoDB's _id
    return queue_dict


@app.get("/queues/", response_model=Queue)
def get_queue(username: str = Query(...)):
    queue = db["queues"].find_one({"username": username})
    if queue is None:
        raise HTTPException(status_code=404, detail="Queue not found")
    return queue


@app.delete("/queues/")
def delete_queue(username: str):
    # Build query based on provided parameters
    delete_result = db["queues"].delete_one({"username": username})
    if delete_result.deleted_count == 1:
        return {"message": "Queue deleted successfully."}
    raise HTTPException(status_code=404, detail="Queue not found")


# Event endpoints
@app.post("/events/{username}/{city}", response_model=Queue)
def create_queue_event(username: str, city: str, event: Event):
    queues_collection = db["queues"]
    buildings_collection = db["buildings"]

    existing_queue = queues_collection.find_one(
        {
            "username": username,  # Match the username
            f"events.{city}": {
                "$exists": True
            },  # Check if the city exists as a key in the events object
        }
    )

    if not existing_queue:
        raise HTTPException(
            status_code=404,
            detail="Queue with the specified username and city not found",
        )
    # Update query to push the new event under the specific city in the events dict
    building = buildings_collection.find_one(
        {"name": event.building_name, "level": event.level}
    )
    result = queues_collection.update_one(
        {"username": username},  # Filter by the username
        {
            "$push": {f"events.{city}": building}
        },  # Push the new event to the city's list
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Couldnt push to user queue")

    # Optionally return the updated queue with the city's events included
    updated_queue = db["queues"].find_one({"username": username})
    return updated_queue


@app.delete("/events/{username}/{city}", response_model=Queue)
def delete_queue_event(username: str, city: str, event: Event):
    queues_collection = db["queues"]

    existing_queue = queues_collection.find_one(
        {
            "username": username,  # Match the username
            f"events.{city}": {
                "$exists": True
            },  # Check if the city exists as a key in the events object
        }
    )

    if not existing_queue:
        raise HTTPException(
            status_code=404,
            detail="Queue with the specified username and city not found",
        )

    # Update query to push the new event under the specific city in the events dict
    filter_query = {
        "username": username,  # Match by username
        f"events.{city}": {  # Check if the city exists in events
            "$elemMatch": {  # Use $elemMatch to filter by array fields
                "name": event.building_name,
                "level": event.level,
            }
        },
    }
    update_operation = {
        "$pull": {  # $pull operator removes elements that match the query
            f"events.{city}": {  # City as the key in events
                "name": event.building_name,
                "level": event.level,
            }
        }
    }
    result = queues_collection.update_one(filter_query, update_operation)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Couldnt push to user queue")

    # Optionally return the updated queue with the city's events included
    updated_queue = db["queues"].find_one({"username": username})
    return updated_queue
