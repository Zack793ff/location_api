from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Define a model for the incoming data
class Location(BaseModel):
    latitude: str
    longitude: str
    timestamp: Optional[str] = None  # Optional timestamp

# In-memory storage for demonstration purposes
# You might use a database in a real-world application
location_data = []

@app.post("/update_location")
async def update_location(location: Location):
    location_data.append(location)
    return {"message": "Location data received successfully", "data": location}

@app.get("/get_locations")
async def get_locations():
    return {"locations": location_data}

def main():
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


if __name__ == '__main__':
    main()
