from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.assignment import find_best_rider
from app.services.route_optimizer import optimize_rider_route

router = APIRouter(prefix="/dispatch", tags=["Dispatch & Routing"])


@router.post("/assign/{order_id}", response_model=schemas.OrderResponse)
def assign_best_rider(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be assigned",
        )

    available_riders = (
        db.query(models.Rider)
        .filter(models.Rider.status == "AVAILABLE")
        .all()
    )

    rider = find_best_rider(order, available_riders)
    if rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available riders found")

    order.rider_id = rider.id
    order.status = "ASSIGNED"

    active_assigned_count = sum(
        1
        for existing_order in rider.orders
        if existing_order.status in {"ASSIGNED", "IN_TRANSIT"}
    )

    if active_assigned_count >= rider.max_active_orders:
        rider.status = "BUSY"

    db.commit()
    db.refresh(order)
    return order


@router.get("/route/{rider_id}")
def get_rider_route(
    rider_id: int,
    db: Session = Depends(get_db),
):
    rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    if rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")

    orders = (
        db.query(models.Order)
        .filter(models.Order.rider_id == rider.id)
        .filter(models.Order.status.in_(["ASSIGNED", "IN_TRANSIT"]))
        .all()
    )

    return optimize_rider_route(rider, orders)