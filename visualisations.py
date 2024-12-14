import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import os


path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + 'fb_scores.db')
cur = conn.cursor()
#might have to use join at some point?


#create list of tuples with id, date
cur.execute(
    "SELECT id, date FROM Date_Keys"
)
dates = cur.fetchall()
days = []
daily_scores = []
for date in dates:
    t_score = 0
    #go through Scores table and find each score that corresponds with that date


    cur.execute(
        'SELECT t_score FROM Scores WHERE date = ?',
        (date[0],)
    )
    score = cur.fetchall()
    #add the scores up for each date
    for tup in score:
        t_score = t_score + tup[0]
    #add to lists with date and score
    days.append(date[1])
    daily_scores.append(t_score)


fig, ax = plt.subplots()
ax.scatter(days, daily_scores)
ax.set_xlabel("Date")
#makes it so you only view every 6th tickmark for readability
ax.set_xticks(days[::15])
ax.set_ylabel("Total Combined Score")
ax.set_title('Score vs Date')
plt.savefig('score_vs_date.png') 
plt.show()


cur.execute('SELECT temperature FROM Weather')
temps = cur.fetchall()
cur.execute('SELECT t_score FROM Scores')
scores = cur.fetchall()
temps_list = []
scores_list = []
i= 0
for temp in temps:
    temps_list.append(temp[0])
    scores_list.append(scores[i][0])
    i+=1
#print(temps_list)
#print(scores)
fig, ax = plt.subplots()
ax.scatter(temps_list, scores_list, color = 'black')
ax.set_ylabel('Score')
ax.set_xlabel('Average Daily Temperature (F)')
ax.set_title('Score vs Average Daily Temperature') 
#ax.set_position([0.28,0.11,0.6,0.6]) 
plt.savefig('score_vs_temp.png') 
plt.show()

cur.execute('SELECT temperature FROM Weather')
temps = cur.fetchall()
cur.execute('SELECT elevation FROM Weather')
elevations = cur.fetchall()
temps_list = []
elevation_list = []
i= 0
for temp in temps:
    temps_list.append(temp[0])
    elevation_list.append(elevations[i][0])
    i+=1
fig, ax = plt.subplots()
ax.scatter(temps_list, elevation_list, color = 'purple')
ax.set_ylabel('Elevation (m)')
ax.set_xlabel('Average Daily Temperature (F)')
ax.set_title('Average Daily Temperature vs Elevation') 
plt.savefig('temp_vs_elevation.png') 
plt.show()

cur.execute('SELECT precipitation FROM Weather')
precipitations = cur.fetchall()
cur.execute('SELECT t_score FROM Scores')
scores = cur.fetchall()
precipitation_list = []
scores_list = []
i= 0
for precipitation in precipitations:
    precipitation_list.append(precipitation[0])
    scores_list.append(scores[i][0])
    i+=1
fig, ax = plt.subplots()
ax.scatter(scores_list, precipitation_list, color = 'red')
ax.set_xlabel('Score')
ax.set_ylabel('Daily Precipitation (mm)')
ax.set_title('Daily Precipitation vs Score') 
#ax.set_position([0.28,0.11,0.6,0.6]) 
plt.savefig('precipitation_vs_score.png') 
plt.show()
