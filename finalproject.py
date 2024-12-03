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
#print(json.dumps(responses, indent=4))

for match in responses['matches']:
    #print(json.dumps(match, indent=4))
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    date = match["utcDate"]
    date = re.search(date_pattern, date)
    date = date.group()
    homeScore = match['score']['fullTime']['home']
    awayScore = match['score']['fullTime']['away']
    total_score = int(homeScore) + int(awayScore)

#get match
#get date and score from match