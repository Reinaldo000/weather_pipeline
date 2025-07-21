from pipeline import get_conn, fetch_station_info, fetch_observations, insert_station, insert_observations

def run_pipeline(station_id):
    conn = get_conn()
    try:
        print("📡 Obteniendo información de estación...")
        station_data = fetch_station_info(station_id)
        insert_station(conn, station_data)

        print("🌦️ Obteniendo observaciones...")
        obs_data = fetch_observations(station_id)
        insert_observations(conn, station_id, obs_data)
        print("✅ Pipeline completado.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Puedes cambiar esta estación si deseas
    run_pipeline("KSEA")
