CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    vendor_id VARCHAR(10),
    
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,

    passenger_count SMALLINT CHECK (passenger_count >= 0),

    pickup_longitude DOUBLE PRECISION,
    pickup_latitude DOUBLE PRECISION,
    dropoff_longitude DOUBLE PRECISION,
    dropoff_latitude DOUBLE PRECISION,

    store_and_fwd_flag BOOLEAN,

    trip_duration INTEGER CHECK (trip_duration >= 0),

    pickup_hour SMALLINT CHECK (pickup_hour >= 0 AND pickup_hour <= 23),
    pickup_weekday SMALLINT CHECK (pickup_weekday >= 0 AND pickup_weekday <= 6),

    trip_distance_km REAL CHECK (trip_distance_km >= 0),
    trip_speed_kmh REAL CHECK (trip_speed_kmh >= 0),

    time_of_day VARCHAR(10)
);

CREATE INDEX idx_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX idx_pickup_hour ON trips(pickup_hour);
CREATE INDEX idx_pickup_weekday ON trips(pickup_weekday);
CREATE INDEX idx_time_of_day ON trips(time_of_day);
CREATE INDEX idx_vendor_id ON trips(vendor_id);
