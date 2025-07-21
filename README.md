# Weather Data Pipeline

This project is a simple ETL (Extract, Transform, Load) pipeline that pulls weather observation data from the [National Weather Service API](https://api.weather.gov), stores it in a PostgreSQL database, and allows querying for basic analytics.

---

## Features

- Connects to the NWS API using a valid `User-Agent` header
- Extracts data from a specific weather station (e.g. `KSEA`)
- Stores:
  - Station metadata
  - Last 7 days of weather observations
- Handles duplicates using constraints
- Includes SQL queries for temperature and wind analytics

---

## Technologies Used

- **Python 3.10+**
- **PostgreSQL**
- **Requests** for HTTP communication
- **psycopg2** for PostgreSQL integration
- **dotenv** for managing configuration

---

## Project Structure

```

weather\_pipeline/
│
├── config.env         # Database credentials (not version-controlled)
├── requirements.txt   # Python dependencies
├── db\_setup.sql       # SQL schema for tables
├── pipeline.py        # Core ETL logic
├── main.py            # Entry point to run the pipeline
└── README.md          # Documentation (this file)

````

---

## Setup Instructions

### 1. Install PostgreSQL and create database

```bash
createdb weather
````

### 2. Create required tables

```bash
psql -U postgres -d weather -f db_setup.sql
```

### 3. Set environment variables

Create a file named `.env` or `config.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather
DB_USER=postgres
DB_PASS=your_password
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the pipeline

```bash
python main.py
```

This fetches station info and 7 days of observations for station `KSEA` and stores them in the database.

---

## What Data is Stored?

### Stations Table

| Field       | Type    |
| ----------- | ------- |
| station\_id | VARCHAR |
| name        | TEXT    |
| timezone    | TEXT    |
| latitude    | FLOAT   |
| longitude   | FLOAT   |

### Observations Table

| Field             | Type        |
| ----------------- | ----------- |
| observation\_time | TIMESTAMPTZ |
| temperature       | FLOAT       |
| wind\_speed       | FLOAT       |
| humidity          | FLOAT       |

Duplicates are avoided using a `UNIQUE(station_id, observation_time)` constraint.

---

## SQL Metrics

### 1. Average observed temperature for last week (Mon–Sun):

```sql
SELECT ROUND(AVG(temperature), 2) AS avg_temperature
FROM observations
WHERE observation_time >= date_trunc('week', current_date - interval '1 week')
  AND observation_time < date_trunc('week', current_date);
```

### 2. Maximum wind speed change between consecutive observations in last 7 days:

```sql
WITH diffs AS (
  SELECT
    observation_time,
    wind_speed,
    wind_speed - LAG(wind_speed) OVER (ORDER BY observation_time) AS diff
  FROM observations
  WHERE observation_time >= now() - interval '7 days'
)
SELECT MAX(ABS(diff)) AS max_wind_change
FROM diffs;
```

---

## Testing

You can change the station ID in `main.py` to test with different locations:

```python
run_pipeline("KSEA")  # e.g., try "KLAX", "KJFK", etc.
```

---

## Notes & Assumptions

* Only the last 7 days of data are processed.
* The pipeline is idempotent and skips duplicate entries.
* This version supports **one station at a time** (can be extended).
* Error handling is minimal and can be improved with logging & retries.

---

