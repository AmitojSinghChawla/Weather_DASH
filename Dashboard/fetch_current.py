from db import get_connected, get_latest_date_time
import pandas as pd
from datetime import datetime, timedelta
from config import CITIES,BACKFILL_MONTHS,current_api
import requests

def start_date(city, table):
    latest = get_latest_date_time(table, city)   # a full timestamp, e.g. 2026-07-27 14:00+00

    if latest is None:
        today = datetime.today()
        backfill_start = today - timedelta(days=30 * BACKFILL_MONTHS)
        return backfill_start.strftime("%Y-%m-%d")
    else:
        # re-fetch from the SAME day the watermark is on (no +1 day).
        # the API gives us that whole day's 24 hours; the hours we already
        # have get skipped by ON CONFLICT, and only 15:00-23:00 are new.
        return latest.strftime("%Y-%m-%d")


def fetch_current_weather(city,lat,long, table,cursor):

    date = start_date(city, table)
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }
    data = requests.get(current_api, params=params)
    data= data.json()
    dataset=pd.DataFrame(data["hourly"])


    if dataset.empty:
        print("No New Data")

    else:
        for row in dataset.itertuples():
            cursor.execute("""
                    INSERT INTO raw_actuals(city,time,
            
            """)























































if __name__ == "__main__":
    for c in CITIES:
