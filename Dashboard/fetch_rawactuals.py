from db import get_connected
from config import weather_api,pollution_api
import os
from dotenv import load_dotenv
import requests
from db import get_or_create_time_id

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")




def get_actuals():
    conn = get_connected()
    cursor = conn.cursor()

    from datetime import datetime, timezone

    timestamp = datetime.now(timezone.utc)
    time_id = get_or_create_time_id(cursor, timestamp)

    cursor.execute("SELECT * FROM locations")
    cities = cursor.fetchall()
    for c in cities:
        location_id = c[0]
        city = c[1]
        latitude = c[4]
        longitude = c[5]
        response1 = requests.get(weather_api,
                             params={'lat': latitude, 'lon': longitude, 'appid': API_KEY, 'units': 'metric'})

        response2 = requests.get(pollution_api,
                             params={'lat': latitude, 'lon': longitude, 'appid': API_KEY, 'units': 'metric'})

        data1 = response1.json()
        data2 = response2.json()
        temperature = data1['main']['temp']
        feels_like = data1['main']['feels_like']
        humidity = data1['main']['humidity']
        wind_speed = data1['wind']['speed']
        pressure = data1['main']['pressure']
        visibility = data1['visibility']
        condition = data1['weather'][0]['main']

        aqi_value = data2['list'][0]['main']['aqi']
        components = data2['list'][0]['components']

        cursor.execute("SELECT weather_condition_id FROM weather_conditions WHERE condition = %s", (condition,))
        condition_id = cursor.fetchone()

        pollutant_values = {
                "PM2.5": components["pm2_5"],
                "PM10": components["pm10"],
                "NO2": components["no2"],
                "SO2": components["so2"],
                "CO": components["co"],
                "O3": components["o3"] }

        for pollutant_name, concentration in pollutant_values.items(): # To loop through a dictionary we need .items()
            cursor.execute("SELECT pollutant_id FROM pollutants WHERE pollutant_name = %s", (pollutant_name,))
            pollutant_id = cursor.fetchone()

            cursor.execute("""
                            INSERT INTO fact_weather_readings(
                            location_id,time_id,pollutant_id,condition_id,temperature,feels_like,humidity,wind_speed,pressure,visibility,aqi_value,pollutant_concentration,fetched_at) 
                            VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW()) ON CONFLICT DO NOTHING ; """ ,
                            (location_id, time_id, pollutant_id, condition_id,temperature, feels_like, humidity, wind_speed,pressure, visibility, aqi_value, concentration))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    get_actuals()
