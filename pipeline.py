import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

# Conexión a la base de datos
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

HEADERS = {
    "User-Agent": "myweatherapp.com, contact@myweatherapp.com"
}

BASE_URL = "https://api.weather.gov"

# Obtener info de estación
def fetch_station_info(station_id):
    r = requests.get(f"{BASE_URL}/stations/{station_id}", headers=HEADERS)
    r.raise_for_status()
    return r.json()

# Obtener observaciones de últimos 7 días
def fetch_observations(station_id):
    start = (datetime.utcnow() - timedelta(days=7)).isoformat()
    url = f"{BASE_URL}/stations/{station_id}/observations"
    r = requests.get(url, headers=HEADERS, params={"start": start})
    r.raise_for_status()
    return r.json()

def insert_station(conn, data):
    props = data["properties"]
    coords = data["geometry"]["coordinates"]
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO stations (station_id, name, timezone, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (station_id) DO NOTHING;
        """, (
            props["stationIdentifier"],
            props["name"],
            props["timeZone"],
            coords[1],
            coords[0]
        ))
    conn.commit()

def insert_observations(conn, station_id, obs_data):
    with conn.cursor() as cur:
        for o in obs_data.get("features", []):
            p = o["properties"]
            try:
                cur.execute("""
                    INSERT INTO observations (station_id, observation_time, temperature, wind_speed, humidity)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    station_id,
                    p["timestamp"],
                    round(p["temperature"]["value"] or 0, 2),
                    round(p["windSpeed"]["value"] or 0, 2),
                    round(p["relativeHumidity"]["value"] or 0, 2)
                ))
            except Exception as e:
                print(f"Error insertando una observación: {e}")
    conn.commit()
