import requests
import json
import matplotlib
import re
import sqlite3
import os

def set_up_fb_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

uri = 'https://api.football-data.org/v4/competitions'
headers = { 'X-Auth-Token': 'c13b0efbe1df4ac68a950a03595a03c0' }

cur, conn = set_up_fb_db("fb_scores.db")


response = requests.get(uri, headers=headers)
competitions = response.json().get('competitions', [])
for competition in competitions:
    if competition['name'] == 'Premier League':
        pleague_id = competition['id']

urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-11-23&dateTo=2024-12-01'

response = requests.get(urid, headers=headers)
responses = response.json()


cur.execute(
    "CREATE TABLE IF NOT EXISTS Date_Keys (id INTEGER PRIMARY KEY, date TEXT)"
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS Scores (date INTEGER, t_score INTEGER)"
)

for match in responses['matches']:
    #gets date
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    date = match["utcDate"]
    date = re.search(date_pattern, date)
    date = date.group()
    #gets scores of home and away teams
    homeScore = int(match['score']['fullTime']['home'])
    awayScore = int(match['score']['fullTime']['away'])
    #gets total goals scored
    total_score = homeScore + awayScore
    #sees if date has already been accessed
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
        cur.execute(
            "INSERT INTO Scores (date, t_score) VALUES (?,?)",
            (date_id, total_score)
        )
        conn.commit()
    else:
        #update the total goals scored for that day
        print(f"Date already exists: {date}")  # Debugging line

        pass
    conn.commit()

    
#how should I limit to 25?




#get match
#get date and score from match