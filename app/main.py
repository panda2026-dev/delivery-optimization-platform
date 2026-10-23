from fastapi import FastAPI
from app.database import engine, Base
import app.models as models
from app.routers import riders, orders, dispatch

# Automatically create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delivery Optimization Platform",
    description="Intelligent Last-Mile Delivery & Route Optimization API",
    version="0.1.0"
)

# Register routers
app.include_router(riders.router)
app.include_router(orders.router)
app.include_router(dispatch.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "online", "message": "Delivery engine backend is running"}