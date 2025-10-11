# Data paths
RAW_DATA = 'data_processing/raw/train.csv'
CLEANED_DATA = 'data_processing/cleaned_trips.csv'
EXCLUDED_DATA = 'data_processing/excluded_records.csv'

# Validation thresholds
NYC_LAT = (40.5, 41.0)
NYC_LON = (-74.3, -73.7)
TRIP_DURATION = (60, 10800)  # 1 min to 3 hours
PASSENGERS = (1, 6)
MAX_SPEED = 100  # km/h