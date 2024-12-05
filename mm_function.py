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

def weather_api(date, latitude, longitude, cur, conn):
    url = "https://archive-api.open-meteo.com/v1/archive"
    querystring = {"latitude": latitude, "longitude": longitude, "start_date": date, "end_date": date, "daily": ["temperature_2m_mean", "precipitation_sum"], "temperature_unit": "fahrenheit"}
    response = requests.get(url, params=querystring)
    response = response.json()
    print(f'{response}')
    elevation = response['elevation']
    temperature = response['daily']['temperature_2m_mean'][0]
    precipitation = response['daily']['precipitation_sum'][0]
    cur.execute(
    "CREATE TABLE IF NOT EXISTS Date_Keys (id INTEGER PRIMARY KEY, date TEXT)"
)
    cur.execute(
    "CREATE TABLE IF NOT EXISTS Weather (date_id INTEGER, latitude FLOAT, longitude FLOAT, elevation FLOAT, temperature FLOAT, precipitation FLOAT)"
)
    cur.execute('SELECT id from Date_Keys WHERE date = ?', (date,))
    #if not
    if cur.fetchone() is None:
        #add date to table
        cur.execute(
            "INSERT INTO Date_Keys (date) VALUES (?)",
            (date,)
        )
        cur.execute('SELECT id FROM Date_Keys WHERE date = ?', (date,))
        date_id = cur.fetchone()[0]
        print(f"Inserted date: {date}, id: {date_id}")  # Debugging line
        #start adding to scores table
    else:
        #update the total goals scored for that day
        print(f"Date already exists: {date}") 
        cur.execute('SELECT id FROM Date_Keys WHERE date = ?', (date,))
        date_id = cur.fetchone()[0] # Debugging line
        


    cur.execute(
            "INSERT INTO Weather (date_id, latitude, longitude, elevation, temperature, precipitation) VALUES (?,?,?,?,?,?)",
            (date_id, latitude, longitude, elevation, temperature, precipitation)
        )
    conn.commit()

#h= set_up_db('football_weather')
cur, conn = set_up_db("football_weather.db")
weather_api('2024-11-15', 42.27, -83.73,cur, conn) 
weather_api('2024-11-15', 50, -99,cur, conn) 
#not sure if duplicate data will be a problem 
#we take out some of the code when combined 
 