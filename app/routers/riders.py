from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(prefix="/riders", tags=["Riders"])


@router.post("/", response_model=schemas.RiderResponse, status_code=status.HTTP_201_CREATED)
def create_rider(
    rider_in: schemas.RiderCreate,
    db: Session = Depends(get_db),
):
    existing_rider = db.query(models.Rider).filter(models.Rider.phone == rider_in.phone).first()
    if existing_rider:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")

    rider = models.Rider(
        name=rider_in.name,
        phone=rider_in.phone,
        current_lat=rider_in.current_lat,
        current_lng=rider_in.current_lng,
        max_active_orders=rider_in.max_active_orders,
    )
    db.add(rider)
    db.commit()
    db.refresh(rider)
    return rider


@router.get("/", response_model=List[schemas.RiderResponse])
def list_riders(
    status: Optional[str] = Query(default=None),
    available_only: bool = False,
    db: Session = Depends(get_db),
):
    query = db.query(models.Rider)

    if status is not None:
        query = query.filter(models.Rider.status == status)

    riders = query.all()

    if available_only:
        riders = [
            rider
            for rider in riders
            if rider.status == "AVAILABLE" and len(rider.orders) < rider.max_active_orders
        ]

    return riders


@router.get("/{rider_id}", response_model=schemas.RiderResponse)
def get_rider(rider_id: int, db: Session = Depends(get_db)):
    rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    if rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")
    return rider


@router.patch("/{rider_id}/location", response_model=schemas.RiderResponse)
def update_rider_location(
    rider_id: int,
    location_update: schemas.RiderLocationUpdate,
    db: Session = Depends(get_db),
):
    rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    if rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")

    rider.current_lat = location_update.current_lat
    rider.current_lng = location_update.current_lng
    db.commit()
    db.refresh(rider)
    return rider