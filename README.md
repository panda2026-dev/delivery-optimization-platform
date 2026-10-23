# Delivery Optimization Platform

A full-stack platform for managing riders, orders, and route optimization in a last-mile delivery system. Built with FastAPI, SQLAlchemy, SQLite/PostgreSQL, and an interactive Leaflet.js map dashboard, this project enables real-time rider tracking, intelligent dispatching, and efficient route planning for delivery operations.

## Overview

This platform supports the core workflows of an on-demand delivery operation:
- Interactive Operations Control Dashboard with live map visualization
- Rider registration, live GPS location tracking, and availability management
- Order creation, assignment, and lifecycle monitoring
- Automatic rider matching using Haversine distance-based scoring
- Route optimization using a nearest-neighbor strategy with pickup-before-dropoff constraints

## Key Features

* **Interactive Operations Dashboard**
  * Real-time map visualization powered by Leaflet.js and OpenStreetMap
  * Sidebar controls to register riders, create delivery orders, and trigger batch auto-dispatching
  * Live status badges and coordinate tracking for all active fleet riders
* **Rider Lifecycle & Live Location Tracking**
  * Maintain rider profiles, vehicle types, status (`AVAILABLE`, `BUSY`), and GPS coordinates
  * Track active order load and capacity constraints
* **Order Management**
  * Create and track orders through states: `PENDING`, `ASSIGNED`, `IN_TRANSIT`, `DELIVERED`, `CANCELLED`
  * Store pickup and dropoff addresses with precise latitude and longitude coordinates
* **Intelligent Auto-Dispatch**
  * Uses Haversine distance calculations to determine the closest available rider
  * Balances rider workload using active assigned order counts
* **Route Optimization**
  * Builds efficient delivery sequences using nearest-neighbor logic
  * Enforces pickup-before-dropoff ordering and calculates cumulative distance and ETA

## Project Structure

```text
delivery-optimization-platform/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── riders.py
│   │   ├── orders.py
│   │   └── dispatch.py
│   └── services/
│       ├── __init__.py
│       ├── distance.py
│       ├── assignment.py
│       └── route_optimizer.py
├── static/
│   └── index.html
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Local Installation & Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Start the development server

```cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Accessing the Platform

* **Operations Control Dashboard (Live Map UI):** `http://127.0.0.1:8000/`
* **Swagger UI (Interactive API Docs):** `http://127.0.0.1:8000/docs`
* **ReDoc (API Reference):** `http://127.0.0.1:8000/redoc`
* **System Health Check:** `http://127.0.0.1:8000/health`

## Docker Execution

To build and run the containerized application:

```cmd
docker compose up --build
```

To stop the services:

```cmd
docker compose down
```

## Testing

Run the automated test suite with:

```cmd
pytest -v
```

This verifies health endpoint functionality, rider creation, order creation, dispatch assignment logic, and route optimization responses.

## Technology Stack

* **Backend:** FastAPI, Python 3.10+, Uvicorn
* **Database & ORM:** SQLite / PostgreSQL, SQLAlchemy, Pydantic v2
* **Frontend:** HTML5, CSS3, JavaScript, Leaflet.js, OpenStreetMap
* **Testing & DevOps:** Pytest, Docker, Docker Compose