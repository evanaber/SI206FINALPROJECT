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
ax.set_xticks(days[::6])
ax.set_ylabel("Total Combined Score")
plt.show()
