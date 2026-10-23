import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_create_rider():
    payload = {
        "name": "Alice Rider",
        "phone": "+919876543210",
        "current_lat": 12.345,
        "current_lng": 67.890,
        "max_active_orders": 3,
    }
    response = client.post("/riders/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["phone"] == payload["phone"]
    assert data["current_lat"] == payload["current_lat"]
    assert data["current_lng"] == payload["current_lng"]
    assert data["status"] == "AVAILABLE"
    assert data["max_active_orders"] == 3


def test_create_order():
    payload = {
        "customer_name": "John Doe",
        "delivery_address": "123 MG Road",
        "pickup_lat": 12.0,
        "pickup_lng": 77.0,
        "drop_lat": 12.1,
        "drop_lng": 77.1,
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == payload["customer_name"]
    assert data["delivery_address"] == payload["delivery_address"]
    assert data["status"] == "PENDING"


def test_auto_dispatch():
    db = TestingSessionLocal()
    rider = models.Rider(
        name="Nearby Rider",
        phone="+919876543211",
        current_lat=12.0,
        current_lng=77.0,
        status="AVAILABLE",
        max_active_orders=3,
    )
    db.add(rider)
    db.commit()
    rider_id = rider.id

    order = models.Order(
        customer_name="Jane Smith",
        delivery_address="45 Brigade Road",
        pickup_lat=12.001,
        pickup_lng=77.001,
        drop_lat=12.01,
        drop_lng=77.01,
        status="PENDING",
    )
    db.add(order)
    db.commit()
    order_id = order.id
    db.close()

    response = client.post(f"/dispatch/assign/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ASSIGNED"
    assert data["rider_id"] == rider_id


def test_route_optimization():
    db = TestingSessionLocal()
    rider = models.Rider(
        name="Route Rider",
        phone="+919876543212",
        current_lat=12.0,
        current_lng=77.0,
        status="AVAILABLE",
        max_active_orders=3,
    )
    db.add(rider)
    db.commit()
    rider_id = rider.id

    order = models.Order(
        customer_name="Route Customer",
        delivery_address="Indiranagar",
        pickup_lat=12.002,
        pickup_lng=77.002,
        drop_lat=12.02,
        drop_lng=77.02,
        status="ASSIGNED",
        rider_id=rider_id,
    )
    db.add(order)
    db.commit()
    db.close()

    response = client.get(f"/dispatch/route/{rider_id}")
    assert response.status_code == 200
    data = response.json()
    assert "stops" in data
    assert isinstance(data["stops"], list)
    assert "total_distance_km" in data
    assert "total_time_mins" in data