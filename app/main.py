import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.routers import riders, orders, dispatch

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delivery Optimization Platform API",
    description="Intelligent last-mile delivery optimization platform with route planning and dispatching.",
    version="1.0.0",
)

# Include API routers without duplicate prefixes
app.include_router(riders.router)
app.include_router(orders.router)
app.include_router(dispatch.router)

# Serve frontend dashboard static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def serve_dashboard():
    dashboard_path = os.path.join("static", "index.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"message": "Delivery Optimization Platform API is active. Visit /docs for Swagger UI."}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy"}