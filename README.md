# Delivery Optimization Platform

A modern API for managing riders, orders, and route optimization in a last-mile delivery system. Built with FastAPI, SQLAlchemy, and SQLite/PostgreSQL, this project enables real-time rider tracking, intelligent dispatching, and efficient route planning for delivery operations.

## Overview

This platform is designed to support the core workflows of a delivery business:

- Rider registration and availability tracking
- Order creation, assignment, and status monitoring
- Automatic rider matching using distance-based scoring
- Route optimization using a nearest-neighbor strategy with pickup-before-dropoff constraints

The solution is ideal for logistics teams, on-demand delivery services, and urban mobility platforms that require fast and efficient dispatch decisions.

## Key Features

- Rider lifecycle & live location tracking
  - Maintain rider profiles, status, and current GPS coordinates
  - Track availability, busy state, and active order load
  - Support rider position updates via API

- Order management
  - Create and track orders through states:
    - PENDING
    - ASSIGNED
    - IN_TRANSIT
    - DELIVERED
    - CANCELLED
  - Store pickup and dropoff locations with precise coordinates

- Intelligent auto-dispatch
  - Uses Haversine distance calculations to determine the closest rider
  - Balances rider workload using active assigned order counts
  - Prioritizes available rider selection to minimize dispatch delay

- Route optimization
  - Builds efficient delivery sequences using nearest-neighbor logic
  - Enforces pickup-before-dropoff ordering
  - Calculates cumulative route distance and ETA in minutes

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
├── tests/
│   └── test_api.py
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── alembic.ini
```

## Local Installation & Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you are setting up a newer environment manually, ensure the project includes dependencies such as:

```bash
pip install fastapi uvicorn sqlalchemy pydantic pytest
```

### 3. Run database bootstrapping / migrations

If the project uses Alembic:

```bash
alembic upgrade head
```

If you are using SQLite for local development and the application creates tables automatically, ensure the app initializes the database on startup or run a bootstrap script if included.

Example:

```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4. Start the development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Docker Execution

This project includes Docker support for local deployment and testing.

### Build and start services

```bash
docker-compose up --build
```

This will build the application container and start the service using the configured Docker Compose setup.

To stop the services:

```bash
docker-compose down
```

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI
Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc
Open:

```text
http://127.0.0.1:8000/redoc
```

These interfaces allow you to explore endpoints, test request payloads, and view response models without external tools.

## Testing

Run the full pytest suite with:

```bash
pytest -v
```

This verifies:

- health endpoint functionality
- rider creation workflows
- order creation
- dispatch assignment logic
- route optimization responses

## Example Use Cases

- Dispatch the nearest rider for a new order
- Update rider GPS coordinates during active delivery shifts
- Track the route sequence for assigned deliveries
- Monitor delivery performance and operational metrics

## Technology Stack

- FastAPI
- SQLAlchemy
- Pydantic v2
- SQLite / PostgreSQL
- Python 3.10+
- Pytest
- Uvicorn
- Docker / Docker Compose

## License

This project is intended for demonstration and internal platform use. Add your preferred license if needed.

## Contributing

Contributions are welcome. Please create a feature branch, implement your changes, and run the tests before submitting a pull request.

---

This README provides a complete starting point for understanding, running, and extending the Delivery Optimization Platform.