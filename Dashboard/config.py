import os
from dotenv import load_dotenv

load_dotenv()
CITIES = [
    {"city": "Delhi", "country": "IN", "lat": 28.65, "lon": 77.23},
    {"city": "Berlin", "country": "DE", "lat": 52.52, "lon": 13.40},
    {"city": "Tokyo", "country": "JP", "lat": 35.68, "lon": 139.69},
    {"city": "Paris", "country": "FR", "lat": 48.85, "lon": 2.35},
    {"city": "Sao Paulo", "country": "BR", "lat": -23.55, "lon": -46.63},
    {"city": "Cairo", "country": "EG", "lat": 30.04, "lon": 31.24},
    {"city": "New York", "country": "US", "lat": 40.71, "lon": -74.01},
    {"city": "Sydney", "country": "AU", "lat": -33.87, "lon": 151.21},
    {"city": "Moscow", "country": "RU", "lat": 55.75, "lon": 37.62},
    {"city": "Nairobi", "country": "KE", "lat": -1.29, "lon": 36.82},
    {"city": "Toronto", "country": "CA", "lat": 43.65, "lon": -79.38},
    {"city": "Mumbai", "country": "IN", "lat": 19.08, "lon": 72.88},
]

weather_api = "https://api.openweathermap.org/data/2.5/weather"
pollution_api = "http://api.openweathermap.org/data/2.5/air_pollution"

BACKFILL_MONTHS = 3

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "market_pulse"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "options": "-c search_path=public"
}

if __name__ == "__main__":
    print(DB_CONFIG)
    print(current_api)
    print(history_api)
