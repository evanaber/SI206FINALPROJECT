import requests
import sqlite3

# Google Places API key
API_KEY = 'AIzaSyA1lp0cMVLR6lUM6k_IAR_E16PYu33XEkc'

# Create SQLite database and table
def setup_coor_database():
    conn = sqlite3.connect('soccer_arenas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SoccerArenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

# Function to get latitude and longitude using Google Places API
def get_coordinates(arena_name):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': arena_name,
        'inputtype': 'textquery',
        'fields': 'geometry',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['candidates'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error fetching data for {arena_name}: {data['status']}")
        return None, None

# Function to store arena data in the database
def store_in_database(arena_name, latitude, longitude):
    conn = sqlite3.connect('soccer_arenas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO SoccerArenas (name, latitude, longitude)
        VALUES (?, ?, ?)
    ''', (arena_name, latitude, longitude))
    conn.commit()
    conn.close()

# Main function to process arena names
def main():
    setup_coor_database()
    print("Enter soccer arena names (type 'exit' to finish):")

    while True:
        arena_name = input("Arena Name: ")
        if arena_name.lower() == 'exit':
            break

        latitude, longitude = get_coordinates(arena_name)
        if latitude is not None and longitude is not None:
            store_in_database(arena_name, latitude, longitude)
            print(f"Stored {arena_name} with coordinates ({latitude}, {longitude})")
        else:
            print(f"Failed to get coordinates for {arena_name}")

if __name__ == "__main__":
    main()