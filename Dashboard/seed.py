import psycopg2
from IPython.core.completer import cursor_to_position
from dotenv import load_dotenv
from config import DB_CONFIG
from db import get_connected
load_dotenv(verbose=True)

def default_values():
    conn = get_connected()
    cursor = conn.cursor()

    # Locations
    cities = [
        ('Delhi', 'Delhi', 'India', 28.61390, 77.20900),
        ('Mumbai', 'Maharashtra', 'India', 19.07600, 72.87770),
        ('Bangalore', 'Karnataka', 'India', 12.97160, 77.59460),
        ('Kolkata', 'West Bengal', 'India', 22.57260, 88.36390),
        ('Chennai', 'Tamil Nadu', 'India', 13.08270, 80.27070),
    ]

    # Pollutants
    pollutants = [
        ('PM2.5', 'µg/m³', 60, 'Particulate Matter Fine'),
        ('PM10', 'µg/m³', 100, 'Particulate Matter Coarse'),
        ('NO2', 'µg/m³', 80, 'Nitrogen Dioxide'),
        ('SO2', 'µg/m³', 80, 'Sulphur Dioxide'),
        ('CO', 'mg/m³', 4, 'Carbon Monoxide'),
        ('O3', 'µg/m³', 180, 'Ozone'),
    ]

    # Weather conditions
    conditions = [
        ('Clear', 'Good'),
        ('Clouds', 'Good'),
        ('Haze', 'Moderate'),
        ('Mist', 'Moderate'),
        ('Fog', 'Poor'),
        ('Smoke', 'Poor'),
        ('Rain', 'Moderate'),
        ('Drizzle', 'Moderate'),
        ('Thunderstorm', 'Severe'),
        ('Dust', 'Severe'),
        ('Sand', 'Severe'),
        ('Snow', 'Moderate'),
    ]
    for city in cities:
        cursor.execute("""
    INSERT INTO locations(city,state,country,latitude,longitude) VALUES(%s,%s,%s,%s,%s) ON CONFLICT (city,country) DO NOTHING;""",city)

    for pollutant in pollutants:
        cursor.execute("""
        INSERT INTO pollutants(pollutant_name,unit,safe_limit,category) VALUES(%s,%s,%s,%s)
        ON CONFLICT (pollutant_name) DO NOTHING; """,pollutant)

    for condition in conditions:
        cursor.execute(""" INSERT INTO weather_conditions(condition,severity_level) VALUES(%s,%s)""", condition)


    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    default_values()




