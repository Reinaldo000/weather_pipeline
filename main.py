from pipeline import get_conn, fetch_station_info, fetch_observations, insert_station, insert_observations

def run_pipeline(station_id):
    conn = get_conn()
    try:
        print("📡 Fetching station info...")
        station_data = fetch_station_info(station_id)
        insert_station(conn, station_data)

        print("🌦️ Fetching observations...")
        obs_data = fetch_observations(station_id)
        insert_observations(conn, station_id, obs_data)
        print("✅ Pipeline completed.")
    finally:
        conn.close()

if __name__ == "__main__":
    run_pipeline("KSEA")  # Example station ID (Seattle)
