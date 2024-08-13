from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn

# Database URL (SQLite)
DATABASE_URL = "sqlite:///./locations.db"

# Set up SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Location model as a table in the database
class LocationModel(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    timestamp = Column(String, index=True)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for incoming data
class Location(BaseModel):
    latitude: str
    longitude: str
    timestamp: Optional[str] = None  # Optional timestamp

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Location Service!"}

# Favicon route (optional)
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}

# Endpoint to update location
@app.post("/update_location", response_model=Location)
async def update_location(location: Location, db: Session = Depends(get_db)):
    db_location = LocationModel(
        latitude=location.latitude,
        longitude=location.longitude,
        timestamp=location.timestamp,
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

# Endpoint to retrieve all locations
@app.get("/get_locations", response_model=List[Location])
async def get_locations(db: Session = Depends(get_db)):
    return db.query(LocationModel).all()

# Run the application
def main():
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)

if __name__ == '__main__':
    main()
