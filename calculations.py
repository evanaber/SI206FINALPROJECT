import sqlite3
import os


path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + 'fb_scores.db')
cur = conn.cursor()

#calculate avg temp for each location
#use join clause for locations
#I think we need a 3rd join clause for weather
#but weather needs to have game ids
cur.execute(
    "SELECT * FROM Scores JOIN Loc_Keys ON Scores.location = Loc_Keys.id"
)
games_locations = cur.fetchall()

#Look at temperature data for each location

loc_temps = {}
total_temp = 0
for tup in games_locations:
    if tup[5] not in loc_temps:
        loc_temps[tup[5]] = 0
        total_temp = 0
    total_temp = total_temp
    loc_temps[tup[5]]
