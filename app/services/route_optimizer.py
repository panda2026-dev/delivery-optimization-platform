from app import models
from app.services.distance import estimate_travel_time, haversine_distance


def optimize_rider_route(rider: models.Rider, orders: list[models.Order]) -> dict:
    if not orders:
        return {
            "rider_id": rider.id,
            "stops": [],
            "total_distance_km": 0.0,
            "total_time_mins": 0.0,
        }

    order_map = {order.id: order for order in orders}

    picked_up = set()
    dropped = set()
    current_lat = rider.current_lat
    current_lng = rider.current_lng
    total_distance_km = 0.0
    route_stops = []

    while True:
        available_stops = []

        for order in orders:
            if order.id in picked_up and order.id not in dropped:
                available_stops.append(
                    {
                        "order_id": order.id,
                        "type": "DROP",
                        "lat": order.drop_lat,
                        "lng": order.drop_lng,
                    }
                )
            elif order.id not in picked_up:
                available_stops.append(
                    {
                        "order_id": order.id,
                        "type": "PICKUP",
                        "lat": order.pickup_lat,
                        "lng": order.pickup_lng,
                    }
                )

        if not available_stops:
            break

        best_stop = None
        best_distance = None

        for stop in available_stops:
            distance = haversine_distance(current_lat, current_lng, stop["lat"], stop["lng"])
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_stop = stop

        if best_stop is None:
            break

        total_distance_km += best_distance
        current_lat = best_stop["lat"]
        current_lng = best_stop["lng"]

        route_stops.append(
            {
                "order_id": best_stop["order_id"],
                "type": best_stop["type"],
                "lat": best_stop["lat"],
                "lng": best_stop["lng"],
                "cumulative_distance_km": round(total_distance_km, 2),
                "estimated_time_mins": round(estimate_travel_time(total_distance_km), 1),
            }
        )

        if best_stop["type"] == "PICKUP":
            picked_up.add(best_stop["order_id"])
        else:
            dropped.add(best_stop["order_id"])

    return {
        "rider_id": rider.id,
        "stops": route_stops,
        "total_distance_km": round(total_distance_km, 2),
        "total_time_mins": round(estimate_travel_time(total_distance_km), 1),
    }