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

#should I make a function to change the date on this to get different data each time I call it?
#urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-11-23&dateTo=2024-12-01'
#urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-11-13&dateTo=2024-11-23'
#urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-23&dateTo=2024-11-01'
#urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-13&dateTo=2024-10-22'
#urid = f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-03&dateTo=2024-10-12'

#If we don't have enough dates, we could do singular matches and keep track of scores that way. Idk how far back
#the data from the API goes.

def set_api(link):
    urid = link
    response = requests.get(urid, headers=headers)
    responses = response.json()
    return responses

#are we not supposed to use these?
cur.execute(
    'DELETE FROM Date_Keys'
)
cur.execute(
    'DELETE FROM Scores'
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS Date_Keys (id INTEGER PRIMARY KEY, date TEXT)"
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS Scores (game_num INTEGER PRIMARY KEY, date INTEGER, t_score INTEGER)"
)
#total score keeps getting too high because we are running the same dates over and over again. 
#I need to access new ones and reset the database each time we run the code from the beginning
def test_dif_dates():
    responses = set_api(f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-11-23&dateTo=2024-12-01')
    find_matches(responses)
    responses = set_api(f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-11-13&dateTo=2024-11-23')
    find_matches(responses)
    responses = set_api(f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-23&dateTo=2024-11-01')
    find_matches(responses)
    responses = set_api(f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-13&dateTo=2024-10-22')
    find_matches(responses)
    responses = set_api(f'https://api.football-data.org/v4/matches?competitions={pleague_id}&dateFrom=2024-10-03&dateTo=2024-10-12')
    find_matches(responses)
# call it with different dates
def find_matches(responses):
    for match in responses['matches']:
    #gets date
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        date = match["utcDate"]
        date = re.search(date_pattern, date)
        date = date.group()
    #gets name of away team for location data
        homeTeam = match['homeTeam']['name']
        venue = team_loc[homeTeam]
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
        cur.execute(
                "INSERT INTO Scores (date, t_score) VALUES (?,?)",
                (date_id, total_score)
            )
        '''
        if 0 = 0:
            cur.execute('SELECT id FROM Date_Keys WHERE date = ?', (date,))
            date_id = cur.fetchone()[0]
        #start adding to scores table
            cur.execute(
                "INSERT INTO Scores (date, t_score) VALUES (?,?)",
                (date_id, total_score)
            )
            conn.commit()
        else:
            cur.execute('SELECT id FROM Date_Keys WHERE date = ?', (date,))
            dateid = cur.fetchone()[0]
            cur.execute('SELECT t_score FROM Scores WHERE date = ?', (dateid,))
            c_score = cur.fetchone()[0] 
            updated_score = int(c_score) + total_score
            cur.execute("UPDATE Scores SET t_score = ? WHERE date = ?",(updated_score, dateid))
        #update the total goals scored for that day
        '''

        conn.commit()
    
#make dictionary to set home team equal to location (city name)
team_loc = {
    'Arsenal FC':'London',
    'Aston Villa FC':'Birmingham',
    'AFC Bournemouth':'Bournemouth',
    'Brentford FC':'London',
    'Brighton & Hove Albion FC':'Brighton',
    'Chelsea FC':'London',
    'Crystal Palace FC':'London',
    'Everton FC':'Liverpool',
    'Fulham FC':'London',
    'Ipswich Town FC':'Ipswich',
    'Leicester City FC':'Leicester',
    'Liverpool FC':'Liverpool',
    'Manchester City FC':'Manchester',
    'Manchester United FC':'Trafford',
    'Newcastle United FC':'Newcastle upon Tyne',
    'Nottingham Forest FC':'West Bridgford',
    'Southampton FC':'Southampton',
    'Tottenham Hotspur FC':'London',
    'West Ham United FC':'London',
    'Wolverhampton Wanderers FC':'Wolverhampton',
}
    
#how should I limit to 25?

def main():
   test_dif_dates()





if __name__ == "__main__":
    main()


#get match
#get date and score from match