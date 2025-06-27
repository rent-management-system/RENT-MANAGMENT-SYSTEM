# Entry point for FastAPI app
from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)