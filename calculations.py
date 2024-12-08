import sqlite3
import os


path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + 'fb_scores.db')
cur = conn.cursor()

cur.execute(
    "SELECT Scores.game_num, Loc_Keys.location, Weather.temperature FROM Scores JOIN Loc_Keys ON Scores.location = Loc_Keys.id JOIN Weather ON Scores.game_num = Weather.game_id"
)
games_locations = cur.fetchall()

loc_temps = {}
total_temp = 0
counter = 0
for tup in games_locations:
    if tup[1] not in loc_temps:
        loc_temps[tup[1]] = (0, 0)
    total_temp, counter = loc_temps[tup[1]]
    counter += 1
    total_temp += tup[2]
    loc_temps[tup[1]] = (total_temp, counter)

loc_avgs = []
for location, tup in loc_temps.items():
    loc_avgs.append((location, tup[0]/tup[1]))

with open('calculations.txt', 'w') as writer:
    for tup in loc_avgs:
        writer.write(f'(Location: {tup[0]}, average gameday temperature: {tup[1]}) \n')
writer.close()
