from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import os
import uvicorn

# --- Configuration ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "host_monitoring"

app = FastAPI()

# --- CORS Middleware FIX (Allows local HTML file to access API) ---
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# --- Models (Updated to reflect new metrics) ---
class Metrics(BaseModel):
    host_id: str
    timestamp: str
    cpu: float
    memory: float
    load_average: dict
    process_count: float
    network: dict
    disk: dict
    processes: list

# --- Endpoints ---

@app.post("/api/ingest")
async def ingest(metrics: Metrics):
    """Ingests metrics data into MongoDB."""
    metrics_dict = metrics.dict()
    await db.host_metrics.insert_one(metrics_dict)
    return {"status": "ok"}

@app.get("/api/hosts")
async def get_hosts():
    """Returns a list of all unique host_ids."""
    hosts = await db.host_metrics.distinct("host_id")
    return {"hosts": hosts}

@app.get("/api/metrics/{host_id}")
async def get_metrics(
    host_id: str,
    start_time: str = Query(None, description="Start timestamp (ISO format)"),
    end_time: str = Query(None, description="End timestamp (ISO format)"),
    limit: int = Query(100, description="Maximum number of records to return")
):
    """Returns metrics for a specific host, optionally filtered by time range."""
    query = {"host_id": host_id}

    time_query = {}
    
    if start_time:
        time_query["$gte"] = start_time
    if end_time:
        time_query["$lte"] = end_time

    if not start_time and not end_time:
        one_day_ago = (datetime.utcnow() - timedelta(hours=24)).isoformat()
        time_query["$gte"] = one_day_ago

    if time_query:
        query["timestamp"] = time_query
    
    cursor = db.host_metrics.find(query).sort("timestamp", -1).limit(limit)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results

@app.get("/api/processes/{host_id}")
async def get_processes(host_id: str):
    """Returns the most recent process list and count for a specific host."""
    # This endpoint grabs the latest document to provide the process list and count
    doc = await db.host_metrics.find_one({"host_id": host_id}, sort=[("timestamp", -1)])
    
    if doc:
        return {
            "host_id": doc["host_id"],
            "timestamp": doc["timestamp"],
            "process_count": doc.get("process_count", 0),
            "processes": doc["processes"]
        }
    return {"host_id": host_id, "processes": []}

@app.get("/")
def read_root():
    return {"status": "Monitoring API is running"}
