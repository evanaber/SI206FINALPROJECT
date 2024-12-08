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

cur, conn = set_up_db("fb_scores.db")

            
def weather_api():
    cur.execute("CREATE TABLE IF NOT EXISTS Date_Keys (id INTEGER PRIMARY KEY, date TEXT)")
    cur.execute(
    "CREATE TABLE IF NOT EXISTS Weather (game_id INTEGER, date_id INTEGER, latitude FLOAT, longitude FLOAT, elevation FLOAT, temperature FLOAT, precipitation FLOAT)"
)
    cur.execute(
        'SELECT latitude FROM Game_Locations'
    )
    latitudes = cur.fetchall()
    cur.execute(
        'SELECT longitude FROM Game_Locations'
    )
    longitudes = cur.fetchall()
    cur.execute(
        'SELECT date_id FROM Game_Locations'
    )
    date_ids = cur.fetchall()
    cur.execute(
        'SELECT game_num FROM Game_Locations'
    )
    game_ids = cur.fetchall()
    try:
        cur.execute(
            'SELECT COUNT(date_id) FROM Weather'
        )
        base = cur.fetchone()[0]
    except:
        base = 0

    for i in range(25):
        index = base + i
        cur.execute(
        'SELECT date FROM Date_Keys WHERE id = ?', (date_ids[index][0],))
        date = cur.fetchone()[0]
        latitude =latitudes[index][0]
        longitude = longitudes[index][0]  
        game_id = game_ids[index][0]  
        url = "https://archive-api.open-meteo.com/v1/archive"
        querystring = {"latitude": latitude, "longitude": longitude, "start_date": date, "end_date": date, "daily": ["temperature_2m_mean", "precipitation_sum"], "temperature_unit": "fahrenheit"}
        response = requests.get(url, params=querystring)
        response = response.json()
        elevation = response['elevation']
        temperature = response['daily']['temperature_2m_mean'][0]
        precipitation = response['daily']['precipitation_sum'][0]
    
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
        else:
        #update the total goals scored for that day
            cur.execute('SELECT id FROM Date_Keys WHERE date = ?', (date,))
            date_id = cur.fetchone()[0] 
        cur.execute(
                "INSERT INTO Weather (game_id, date_id, latitude, longitude, elevation, temperature, precipitation) VALUES (?,?,?,?,?,?,?)",
                (game_id, date_id, latitude, longitude, elevation, temperature, precipitation)
            )
        conn.commit()

def main():
    weather_api()
   


if __name__ == "__main__":
    main()


 