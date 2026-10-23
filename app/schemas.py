from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RiderBase(BaseModel):
    name: str
    phone: str
    current_lat: float
    current_lng: float
    max_active_orders: int = 3


class RiderCreate(RiderBase):
    pass


class RiderLocationUpdate(BaseModel):
    current_lat: float
    current_lng: float


class RiderResponse(RiderBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    customer_name: str
    delivery_address: str
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    status: str
    rider_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)