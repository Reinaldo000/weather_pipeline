CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR PRIMARY KEY,
    name TEXT,
    timezone TEXT,
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR REFERENCES stations(station_id),
    observation_time TIMESTAMPTZ,
    temperature FLOAT,
    wind_speed FLOAT,
    humidity FLOAT,
    UNIQUE(station_id, observation_time)
);
