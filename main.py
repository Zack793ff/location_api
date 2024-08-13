from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Model for the incoming data
class Location(BaseModel):
    latitude: str
    longitude: str
    timestamp: Optional[str] = None  # Optional timestamp

# In-memory storage for demonstration purposes
location_data = []

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Location Service!"}

# Favicon route (optional)
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

# Endpoint to update location
@app.post("/update_location")
async def update_location(location: Location):
    location_data.append(location)
    return {"message": "Location data received successfully", "data": location}

# Endpoint to retrieve all locations
@app.get("/get_locations")
async def get_locations():
    return {"locations": location_data}

def main():
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)

if __name__ == '__main__':
    main()
