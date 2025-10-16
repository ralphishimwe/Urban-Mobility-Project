def detect_speed_anomalies(trips, speed_threshold=150):
   
    valid_trips = []
    anomalies = []

    for trip in trips:
        try:
            distance = float(trip['trip_distance_km'])  # in km
            duration = float(trip['trip_duration']) / 3600  # seconds to hours

            if duration == 0:
                anomalies.append(trip)
                continue

            speed = distance / duration  # km/h

            if speed > speed_threshold:
                anomalies.append(trip)
            else:
                valid_trips.append(trip)
        except (ValueError, ZeroDivisionError, KeyError):
            anomalies.append(trip)

    return valid_trips, anomalies
