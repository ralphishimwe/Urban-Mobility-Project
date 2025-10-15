import csv
import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),  # default to 5432 if not set
    "sslmode": "require"
}

# Dynamically build path to CSV (relative to this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "..", "data_processing", "cleaned_trips.csv")

def load_data():
    """Load data from cleaned CSV file."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")
    
    print(f"✅ Loading data from: {CSV_PATH}")
    
    records = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        next(reader) 
        for row in reader:
            if not row or len(row) != 16:
                continue  # skip empty or malformed rows

            (
                id,
                vendor_id,
                pickup_datetime,
                dropoff_datetime,
                passenger_count,
                pickup_longitude,
                pickup_latitude,
                dropoff_longitude,
                dropoff_latitude,
                store_and_fwd_flag,
                trip_duration,
                pickup_hour,
                pickup_weekday,
                trip_distance_km,
                trip_speed_kmh,
                time_of_day
            ) = row

            # Convert data types
            records.append((
                id,
                int(vendor_id),
                pickup_datetime,
                dropoff_datetime,
                int(passenger_count),
                float(pickup_longitude),
                float(pickup_latitude),
                float(dropoff_longitude),
                float(dropoff_latitude),
                store_and_fwd_flag,
                int(trip_duration),
                int(pickup_hour),
                int(pickup_weekday),
                float(trip_distance_km),
                float(trip_speed_kmh),
                time_of_day
            ))
    print(f"✅ Loaded {len(records)} rows from CSV.")
    return records

def insert_data(records):
    """Insert records into the 'trips' table in Neon."""
    try:
        print("🔌 Connecting to Neon database...")
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Optional: verify connection
        cur.execute("SELECT current_database(), current_user;")
        db_name, user = cur.fetchone()
        print(f"✅ Connected to DB: '{db_name}' as user: '{user}'")
        
        # Insert query
        insert_query = """
            INSERT INTO trips (
                id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
                pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
                store_and_fwd_flag, trip_duration, pickup_hour, pickup_weekday,
                trip_distance_km, trip_speed_kmh, time_of_day
            ) VALUES %s
            ON CONFLICT (id) DO NOTHING
        """
        
        print(f"📤 Inserting {len(records)} records into 'trips' table...")
        execute_values(cur, insert_query, records)
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Successfully inserted {len(records)} records into 'trips'.")
        
    except Exception as e:
        print(f"❌ Error during database operation: {e}")
        raise

def verify_count():
    """Verify how many rows are in the 'trips' table."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM trips;")
        count = cur.fetchone()[0]
        print(f"📊 Total rows in 'trips' table: {count}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Could not verify row count: {e}")

if __name__ == "__main__":
    try:
        data = load_data()
        if not data:
            print("⚠️ No data loaded. Check your CSV file.")
        else:
            insert_data(data)
            verify_count()
    except Exception as e:
        print(f"💥 Script failed: {e}")