# NYC Taxi Trip Data - Data Processing & Cleaning
This project processes and cleans the NYC Taxi Trip dataset for analysis and database storage.

## Data processing Structure
Urban-Mobility-Project/
├── data_processing/
│   ├── raw/
│   │   └── train.csv              # Sample raw data (not complete dataset)
│   ├── clean_data.py              # Main cleaning script
│   ├── utils.py                   # Helper functions
│   ├── config.py                  # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   ├── cleaned_trips.csv          # Output: Cleaned data (generated after running)
│   └── excluded_records.csv       # Output: Removed records log (generated after running)
└── README.md

## Important Note About Dataset

**The `train.csv` file in this repository contains only a SAMPLE of the dataset** because:
- The complete raw dataset is over 100 MB
- GitHub does not allow files larger than 100 MB to be committed

### To get the full dataset:
1. Download from Kaggle: [NYC Taxi Trip Duration Dataset](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data?select=train.zip)
2. Extract `train.zip`
3. Place the full `train.csv` file in the `data_processing/raw/` folder
4. Run the cleaning script

## 🚀 Setup Instructions

### Installation Steps

1. **Clone the repository**
   git clone https://github.com/ralphishimwe/Urban-Mobility-Project
   cd Urban-Mobility-Project

2. **Install dependencies**
   pip install -r data_processing/requirements.txt
   Or
   install manually: pip install pandas==2.0.3 numpy==1.24.3


3. **Download the full dataset** (if needed)
   - Visit: https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data?select=train.zip
   - Download `train.zip`
   - Extract and place `train.csv` in `data_processing/raw/`

4. **Run the data cleaning script**
   cd data_processing
   python clean_data.py

### Data Cleaning Steps:
1. Removes rows with missing values
2. Removes duplicate trip records
3. Validates NYC geographic boundaries (latitude: 40.5-41.0, longitude: -74.3 to -73.7)
4. Filters trip duration (1 minute to 3 hours)
5. Validates passenger count (1-6 passengers)
6. Removes trips with unrealistic speeds (>100 km/h)

### Derived Features Created:
1. **trip_distance_km** - Distance in kilometers calculated using Haversine formula
2. **trip_speed_kmh** - Average trip speed in km/h
3. **time_of_day** - Time category (Night/Morning/Afternoon/Evening)

##  Output Files

After running the script, you will get:

1. **cleaned_trips.csv** - Clean dataset ready for database import
2. **excluded_records.csv** - Log of all removed records for transparency


## Troubleshooting
**Issue**: `FileNotFoundError: train.csv not found`
- **Solution**: Make sure `train.csv` is in `data_processing/raw/` folder

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Script runs but produces very few records
- **Solution**: You might be using the sample data. Download the full dataset from Kaggle.

## Notes
- The sample `train.csv` included has only over 400 records for testing purposes
- The full dataset contains over 1.4 million trip records