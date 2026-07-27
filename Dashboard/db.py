import psycopg2
from dotenv import load_dotenv
from config import DB_CONFIG

load_dotenv()


def get_connected():
    """Connect to the PostgreSQL database server on cloud using the neon database service
    earlier we were using local postgresql database."""

    config = DB_CONFIG.copy()
    config["sslmode"] = "require"
    return psycopg2.connect(**config)


def create_tables():
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations(
    
    location_id         SERIAL PRIMARY KEY,
    city                VARCHAR,
    state               VARCHAR,
    country             VARCHAR,
    latitude            NUMERIC(8,5) NOT NULL,
    longitude           NUMERIC(8,5) NOT NULL,
    UNIQUE(city,country)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time(
    time_id             SERIAL PRIMARY KEY,
    timestamp           TIMESTAMPTZ NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pollutants(
    pollutant_id      SERIAL PRIMARY KEY,
    pollutant_name    VARCHAR,
    unit              VARCHAR,
    safe_limit        NUMERIC,
    category          VARCHAR
    ); """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_conditions(
    weather_condition_id            SERIAL PRIMARY KEY,
    condition                       VARCHAR,
    severity_level                  VARCHAR
    );   
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS fact_weather_readings(
    reading_id                      SERIAL PRIMARY KEY,
    location_id                     INTEGER REFERENCES locations(location_id),
    time_id                         INTEGER REFERENCES time(time_id),
    pollutant_id                    INTEGER REFERENCES pollutants(pollutant_id),
    condition_id                    INTEGER REFERENCES weather_conditions(weather_condition_id),
    temperature                     NUMERIC(5,2) ,
    feels_like                      NUMERIC(5,2),
    humidity                        NUMERIC(5,2),
    wind_speed                      NUMERIC(5,2),
    pressure                        NUMERIC(5,2),
    visibility                      NUMERIC(5,2) ,  
    aqi_value                       INTEGER,
    pollutant_concentration         NUMERIC(5,2) ,
    fetched_at                      TIMESTAMPTZ ,
    
    UNIQUE(location_id, time_id,pollutant_id)
    );
    """)

    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_fact_location ON fact_weather_readings (location_id);"""
    )
    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_fact_time ON fact_weather_readings (time_id);"""
    )
    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_fact_pollutant ON fact_weather_readings (pollutant_id);"""
    )
    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_fact_condition ON fact_weather_readings (condition_id);"""
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created")


if __name__ == "__main__":
    create_tables()
