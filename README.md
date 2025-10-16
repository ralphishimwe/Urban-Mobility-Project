# NYC Taxi Analytics Dashboard

A full-stack web application for analyzing NYC taxi trip data with interactive visualizations and filtering capabilities.

## Prerequisites

1. Python 3.9+ installed
2. PostgreSQL database (You can use a local PostgreSQL or a cloud service like Neon)
3. Git installed

## Step-by-Step Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/ralphishimwe/Urban-Mobility-Project.git
cd Urban-Mobility-Project
```

### 2. Set Up the Database

1. Create a PostgreSQL database for the project
2. Create a `.env` file in the project root with your database credentials:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_NAME=your_database_name
DB_PORT=5432  # Default PostgreSQL port
```

### 3. Set Up the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install required Python packages:
```bash
pip3 install fastapi uvicorn[standard] sqlalchemy python-dotenv psycopg2-binary
```

3. Load the data into the database:
```bash
python3 load_data.py
```
This script will:
- Read the cleaned trip data from `data_processing/cleaned_trips.csv`
- Create the necessary database tables
- Import the data into your PostgreSQL database

4. Start the backend server:
```bash
python3 -m uvicorn main:app --reload --port 8080
```
The backend API will be available at http://127.0.0.1:8080

### 4. Set Up the Frontend

1. Open a new terminal and navigate to the frontend directory:
```bash
cd front_end
```

2. Start a simple HTTP server:
```bash
python3 -m http.server 3000
```
The frontend will be available at http://127.0.0.1:3000

## Using the Application

1. Open your web browser and go to http://127.0.0.1:3000
2. You should see the NYC Taxi Analytics Dashboard with:
   - Overall statistics at the top
   - Interactive filters panel
   - Data table showing trip details
   - Visualizations of the data

### Available Features

1. View overall statistics:
   - Total number of trips
   - Average trip distance
   - Average trip speed
   - Average trip duration

2. Filter data by:
   - Number of trips to display
   - Pickup hour (0-23)
   - Weekday (Monday-Sunday)
   - Time of day
   - Trip duration range
   - Trip speed range
   - Trip distance range

3. Interactive visualizations:
   - Hourly distribution of trips
   - Weekly patterns
   - Trip statistics charts

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: http://127.0.0.1:8080/docs
- ReDoc: http://127.0.0.1:8080/redoc

## Troubleshooting

1. If you see a database connection error:
   - Verify your database credentials in the `.env` file
   - Ensure your database server is running
   - Check if you can connect to the database using a GUI tool

2. If the frontend shows no data:
   - Check if both backend and frontend servers are running
   - Open browser developer tools (F12) and check the Console for errors
   - Verify that the backend URL in `front_end/script.js` matches your backend server
   - Ensure the data was properly loaded using `load_data.py`

3. If you get a "port already in use" error:
   - Change the port number in the server start commands
   - Kill any process using the required port:
     ```bash
     lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9
     ```

## Project Structure

```
Urban-Mobility-Project/
├── backend/
│   ├── database_schema.sql
│   ├── load_data.py
│   ├── main.py
│   └── requirements.txt
├── data_processing/
│   ├── clean_data.py
│   ├── cleaned_trips.csv
│   ├── config.py
│   └── utils.py
└── front_end/
    ├── index.html
    ├── script.js
    └── styles.css
```
