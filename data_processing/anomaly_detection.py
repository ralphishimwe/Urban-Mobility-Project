class AnomalyDetector:
    
    def __init__(self, multiplier=1.5):
        self.multiplier = multiplier
    
    def quicksort(self, arr):
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return self.quicksort(left) + middle + self.quicksort(right)
    
    def get_quartile(self, sorted_arr, q):
        """Calculate quartile manually"""
        n = len(sorted_arr)
        pos = q * (n - 1)
        lower = int(pos)
        upper = lower + 1
        
        if upper >= n:
            return sorted_arr[-1]
        
        weight = pos - lower
        return sorted_arr[lower] * (1 - weight) + sorted_arr[upper] * weight
    
    def detect_outliers(self, values):
        if len(values) == 0:
            return [], []
        
        sorted_vals = self.quicksort(values)
        
        q1 = self.get_quartile(sorted_vals, 0.25)
        q3 = self.get_quartile(sorted_vals, 0.75)
        iqr = q3 - q1
        
        lower = q1 - self.multiplier * iqr
        upper = q3 + self.multiplier * iqr
        
        clean_idx = []
        outlier_idx = []
        
        for i in range(len(values)):
            if values[i] < lower or values[i] > upper:
                outlier_idx.append(i)
            else:
                clean_idx.append(i)
        
        return clean_idx, outlier_idx


def detect_speed_anomalies(df):
    """anomaly detection to trip speeds"""
    detector = AnomalyDetector(multiplier=1.5)
    speeds = df['trip_speed_kmh'].tolist()
    clean_idx, outlier_idx = detector.detect_outliers(speeds)
    return clean_idx, outlier_idx
