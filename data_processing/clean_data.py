import pandas as pd
import utils

def clean_data(df):
    """Clean and validate data with all checks"""
    print(f"Starting with {len(df)} records")
    
    # Remove missing values and duplicates
    df = df.dropna()
    df = df.drop_duplicates(subset=[col for col in df.columns if col != 'id'])
    
    # Validate coordinates (NYC boundaries)
    df = df[(df['pickup_latitude'].between(40.5, 41.0)) & 
            (df['pickup_longitude'].between(-74.3, -73.7)) &
            (df['dropoff_latitude'].between(40.5, 41.0)) & 
            (df['dropoff_longitude'].between(-74.3, -73.7))]
    
    # Validate trip duration (1 min to 3 hours) and passengers (1-6)
    df = df[(df['trip_duration'].between(60, 10800)) & 
            (df['passenger_count'].between(1, 6))]
    
    print(f"After cleaning: {len(df)} records")
    return df

def add_features(df):
    """Add derived features"""
    # Format timestamps and extract time components
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_weekday'] = df['pickup_datetime'].dt.dayofweek
    
    # Feature 1: Trip distance (km) using Haversine formula
    df['trip_distance_km'] = df.apply(lambda row: utils.haversine_distance(
        row['pickup_latitude'], row['pickup_longitude'],
        row['dropoff_latitude'], row['dropoff_longitude']), axis=1)
    
    # Feature 2: Trip speed (km/h)
    df['trip_speed_kmh'] = (df['trip_distance_km'] / df['trip_duration']) * 3600
    df = df[df['trip_speed_kmh'] <= 100]  # Remove unrealistic speeds
    
    # Feature 3: Time of day category
    df['time_of_day'] = df['pickup_hour'].apply(utils.categorize_time_of_day)
    
    return df

def main():
    print("="*50)
    print("NYC TAXI DATA CLEANING")
    print("="*50)
    
    # Load and clean
    df_original = pd.read_csv('data_processing/raw/train.csv')
    df = clean_data(df_original.copy())
    df = add_features(df)
    
    # Save outputs
    df.to_csv('data_processing/cleaned_trips.csv', index=False)
    
    # Log excluded records
    excluded_ids = set(df_original['id']) - set(df['id'])
    excluded = df_original[df_original['id'].isin(excluded_ids)]
    excluded.to_csv('data_processing/excluded_records.csv', index=False)
    
    # Summary
    print(f"\nOriginal: {len(df_original)} | Cleaned: {len(df)} | Excluded: {len(excluded)}")
    print(f"Retention: {(len(df)/len(df_original))*100:.2f}%")
    print("\nNew columns:", df.columns.tolist())
    print("\nSample data:")
    print(df.head())
    print("\n" + "="*50)
    print("Cleaning completed!")

if __name__ == "__main__":
    main()