from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?sslmode=require"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
app = FastAPI(
    title="Urban Mobility Backend API",
    description="Backend service for NYC Taxi Trip data analysis.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Urban Mobility API is running!", "docs": "/docs"}

# ───────────────────────────────
# 1. GET /api/trips
# ───────────────────────────────
@app.get("/api/trips")
def get_trips(
    limit: int = Query(100, ge=1, le=1000, description="Number of trips to return (max 1000)"),
    pickup_hour: int = Query(None, ge=0, le=23, description="Filter by hour of day (0–23)"),
    pickup_weekday: int = Query(None, ge=0, le=6, description="Filter by weekday (0=Mon, 6=Sun)"),
    time_of_day: str = Query(None, description="Filter by time of day (e.g., 'morning', 'evening')"),
    min_duration: int = Query(None, ge=0, description="Minimum trip duration (seconds)"),
    max_duration: int = Query(None, ge=0, description="Maximum trip duration (seconds)"),
    min_speed: float = Query(None, ge=0, description="Minimum trip speed (km/h)"),
    max_speed: float = Query(None, ge=0, description="Maximum trip speed (km/h)"),
    min_distance: float = Query(None, ge=0, description="Minimum trip distance (km)"),
    max_distance: float = Query(None, ge=0, description="Maximum trip distance (km)")
):
    # Build dynamic WHERE clause
    filters = []
    params = {"limit": limit}

    if pickup_hour is not None:
        filters.append("pickup_hour = :pickup_hour")
        params["pickup_hour"] = pickup_hour

    if pickup_weekday is not None:
        filters.append("pickup_weekday = :pickup_weekday")
        params["pickup_weekday"] = pickup_weekday

    if time_of_day:
        filters.append("time_of_day = :time_of_day")
        params["time_of_day"] = time_of_day

    if min_duration is not None:
        filters.append("trip_duration >= :min_duration")
        params["min_duration"] = min_duration

    if max_duration is not None:
        filters.append("trip_duration <= :max_duration")
        params["max_duration"] = max_duration

    if min_speed is not None:
        filters.append("trip_speed_kmh >= :min_speed")
        params["min_speed"] = min_speed

    if max_speed is not None:
        filters.append("trip_speed_kmh <= :max_speed")
        params["max_speed"] = max_speed

    if min_distance is not None:
        filters.append("trip_distance_km >= :min_distance")
        params["min_distance"] = min_distance

    if max_distance is not None:
        filters.append("trip_distance_km <= :max_distance")
        params["max_distance"] = max_distance

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""
    query = f"""
        SELECT 
            id, vendor_id, passenger_count,
            pickup_datetime, dropoff_datetime,
            pickup_longitude, pickup_latitude,
            dropoff_longitude, dropoff_latitude,
            store_and_fwd_flag,
            trip_duration, pickup_hour, pickup_weekday,
            trip_distance_km, trip_speed_kmh, time_of_day
        FROM trips
        {where_clause}
        ORDER BY pickup_datetime DESC
        LIMIT :limit
    """

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        trips = [dict(row._mapping) for row in result]
    return trips

# ───────────────────────────────
# 2. GET /api/trips/{id}
# ───────────────────────────────
@app.get("/api/trips/{trip_id}")
def get_trip(trip_id: str):
    query = "SELECT * FROM trips WHERE id = :id"
    with engine.connect() as conn:
        result = conn.execute(text(query), {"id": trip_id})
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Trip not found")
        return dict(row._mapping)

# ───────────────────────────────
# 3. GET /api/stats
# ───────────────────────────────
@app.get("/api/stats")
def get_stats():
    query = """
        SELECT
            COUNT(*) AS total_trips,
            ROUND(AVG(trip_duration), 2) AS avg_trip_duration_sec,
            ROUND(AVG(trip_distance_km), 2) AS avg_trip_distance_km,
            ROUND(AVG(trip_speed_kmh), 2) AS avg_trip_speed_kmh,
            MODE() WITHIN GROUP (ORDER BY pickup_hour) AS most_active_hour,
            MODE() WITHIN GROUP (ORDER BY pickup_weekday) AS most_active_weekday
        FROM trips
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        stats = dict(result.fetchone()._mapping)
    return stats