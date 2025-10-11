### Derived Features Justification (for your report):
1. Trip Distance (km) - Haversine Formula

Why: The dataset doesn't include distance, only coordinates. Distance is essential for analyzing fare efficiency, route optimization, and detecting anomalies.
How: Calculated using Haversine formula between pickup/dropoff GPS coordinates.

2. Trip Speed (km/h)

Why: Helps identify unrealistic trips (too fast = data error), understand traffic patterns, and detect potential fraud.
How: Calculated as (distance / duration) × 3600. Filtered out speeds > 100 km/h as unrealistic for NYC traffic.

3. Time of Day Category

Why: Urban mobility patterns differ drastically by time (rush hour vs night). Enables analysis of demand patterns and pricing strategies.
How: Categorized pickup hour into Night (0-6), Morning (6-12), Afternoon (12-18), Evening (18-24).