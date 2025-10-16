import pandas as pd
import utils
from anomaly_detection import detect_speed_anomalies

def clean_data(df):
    """Clean and validate data"""
    print(f"Starting with {len(df)} records")

    df = df.dropna()
    df = df.drop_duplicates(subset=[col for col in df.columns if col != 'id'])

    df = df[(df['pickup_latitude'].between(40.5, 41.0)) & 
            (df['pickup_longitude'].between(-74.3, -73.7)) &
            (df['dropoff_latitude'].between(40.5, 41.0)) & 
            (df['dropoff_longitude'].between(-74.3, -73.7))]

    df = df[(df['trip_duration'].between(60, 10800)) & 
            (df['passenger_count'].between(1, 6))]
    
    print(f"After cleaning: {len(df)} records")
    return df

def add_features(df):
    """Add derived features"""
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_weekday'] = df['pickup_datetime'].dt.dayofweek

    df['trip_distance_km'] = df.apply(lambda row: utils.haversine_distance(
        row['pickup_latitude'], row['pickup_longitude'],
        row['dropoff_latitude'], row['dropoff_longitude']), axis=1)
    
    df['trip_speed_kmh'] = (df['trip_distance_km'] / df['trip_duration']) * 3600

    df['time_of_day'] = df['pickup_hour'].apply(utils.categorize_time_of_day)
    
    return df

def main():
    print("="*50)
    print("NYC TAXI DATA CLEANING")
    print("="*50)

    df_original = pd.read_csv('data_processing/raw/train.csv')
    df = clean_data(df_original.copy())
    df = add_features(df)

    df_reset = df.reset_index(drop=True)
    clean_idx, outlier_idx = detect_speed_anomalies(df_reset)
    
    df_final = df_reset.iloc[clean_idx]
    df_anomalies = df_reset.iloc[outlier_idx]
    
    print(f"\nAnomaly Detection: {len(outlier_idx)} outliers removed")

    df_final.to_csv('data_processing/cleaned_trips.csv', index=False)
    df_anomalies.to_csv('data_processing/anomalies.csv', index=False)
    
    excluded_ids = set(df_original['id']) - set(df_final['id'])
    excluded = df_original[df_original['id'].isin(excluded_ids)]
    excluded.to_csv('data_processing/excluded_records.csv', index=False)

    print(f"\nFinal: {len(df_final)} records ({(len(df_final)/len(df_original))*100:.1f}% retained)")
    print("\nCleaning completed!")

if __name__ == "__main__":
    main()