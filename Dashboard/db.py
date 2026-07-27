import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG
from dotenv import load_dotenv
import pandas as pd

load_dotenv(verbose=True)


def get_connected():
    """Connect to the PostgreSQL database server on cloud using the neon database service
    earlier we were using local postgresql database."""
    config = DB_CONFIG.copy()
    return psycopg2.connect(**config)


def create_tables():
    """Create the tables in the database."""
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_actuals (
    id SERIAL PRIMARY KEY,
    city                VARCHAR(255),
    target_time         TIMESTAMPTZ NOT NULL,
    actual_temp         NUMERIC,
    actual_humidity     NUMERIC,
    actual_wind         NUMERIC,
    fetched_at          TIMESTAMPTZ NOT NULL,
    UNIQUE(city, target_time)
    );
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_forecasts (
                id                 SERIAL PRIMARY KEY,
                city               VARCHAR      NOT NULL,
                target_time        TIMESTAMPTZ  NOT NULL,
                lead_days          INTEGER      NOT NULL,
                predicted_temp     NUMERIC,
                predicted_humidity NUMERIC,
                predicted_wind     NUMERIC,
                fetched_at         TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (city, target_time, lead_days)
            );
        """)

    cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_actuals_city_time
            ON raw_actuals (city, target_time);
        """)
    cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_forecasts_city_time
            ON raw_forecasts (city, target_time);
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print("TABLES CREATED")


def get_latest_date_time(table, city):
    """
    The watermark. Returns the newest target_time we already stored for
    this city in the given table, or None if we have nothing yet.
    """
    conn = get_connected()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(target_time) FROM {table} WHERE city = %s", (city,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

def show_tables():
    conn = get_connected()
    cursor = conn.cursor()

    tables = pd.read_sql_query("SELECT * FROM raw_actuals", conn)
    for table in tables:
        print(table)









if __name__ == "__main__":
    try:
        create_tables()
    except psycopg2.Error as e:
        print(e)
