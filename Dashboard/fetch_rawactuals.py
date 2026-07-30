
from db import get_connected
import pandas as pd
from config import weather_api,pollution_api
import os
from dotenv import load_dotenv
load_dotenv()
import requests



conn = get_connected()
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM locations")
    cities = cursor.fetchall()
    for c in cities:
        location_id = c[0]
        city = c[1]
        latitude = c[4]
        longitude = c[5]

    API_KEY = os.getenv("WEATHER_API_KEY")
    response1 = requests.get(weather_api,params={'lat':latitude,'lon':longitude,'appid':API_KEY, 'units':'metric'})
    response2 = requests.get(pollution_api,params={'lat':latitude,'lon':longitude,'appid':API_KEY, 'units':'metric'})
    print(response1.json())
    print(response2.json())

except Exception as e:
    print(e)




def get_actuals():
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM locations")
    cities = cursor.fetchall()
