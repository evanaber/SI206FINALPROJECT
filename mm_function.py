import requests
import json
import matplotlib
import re
import sqlite3
import os

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def weather_api(dates, place):
    weather_api_key = f"2212ddc784060812ce08fdf3b5b692ec"
    semi = ";"
    api_date = semi.join(dates)
    url = "https://api.weatherstack.com/historical?access_key={weather_api_key}"
    querystring = {f"query":{place}, "historical_date":{api_date}}
    response = requests.get(url, params=querystring)
    print(response.json())
    for date in dates:
        weather_data = response["historical"][date]
        avgtemp = weather_data["avgtemp"]
        uv_index = weather_data["uv_index"]
    
