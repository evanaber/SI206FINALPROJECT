import requests
import json
import matplotlib

uri = 'https://api.football-data.org/v4/competitions'
headers = { 'X-Auth-Token': 'c13b0efbe1df4ac68a950a03595a03c0' }

response = requests.get(uri, headers=headers)
competitions = response.json().get('competitions', [])
for competition in competitions:
    if competition['name'] == 'Premier League':
        pleague_id = competition['id']
print (pleague_id)
'''
for match in response.json()['matches']:
    print({match['id']})
    print(json.dumps(match, indent=4))
'''
#get match
#get date and score from match