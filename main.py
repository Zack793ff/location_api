from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./locations.db"
engine = create_engine(DATABASE_URL, echo=True)

# Define the Location model
class Location(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    latitude: str
    longitude: str
    timestamp: Optional[str] = None

# Create the tables in the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# FastAPI instance
app = FastAPI()

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

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
async def update_location(location: Location, session: Session = Depends(get_session)):
    session.add(location)
    session.commit()
    session.refresh(location)
    return location

# Endpoint to retrieve all locations
@app.get("/get_locations", response_model=List[Location])
async def get_locations(session: Session = Depends(get_session)):
    statement = select(Location)
    results = session.exec(statement).all()
    return results

# Run the application
def main():
    create_db_and_tables()
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)

if __name__ == '__main__':
    main()
