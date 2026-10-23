from app import models
from app.services.distance import haversine_distance


def find_best_rider(
    order: models.Order,
    available_riders: list[models.Rider],
) -> models.Rider | None:
    if not available_riders:
        return None

    def active_assigned_order_count(rider: models.Rider) -> int:
        rider_orders = getattr(rider, "orders", []) or []
        return sum(
            1 for existing_order in rider_orders if existing_order.status in {"ASSIGNED", "IN_TRANSIT"}
        )

    best_rider = None
    best_score = None

    for rider in available_riders:
        distance_km = haversine_distance(
            rider.current_lat,
            rider.current_lng,
            order.pickup_lat,
            order.pickup_lng,
        )
        active_orders = active_assigned_order_count(rider)

        score = (distance_km, active_orders)

        if best_score is None or score < best_score:
            best_score = score
            best_rider = rider

    return best_rider