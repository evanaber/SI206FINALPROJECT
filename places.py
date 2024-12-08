import os
import requests
import sqlite3

API_KEY = 'AIzaSyA1lp0cMVLR6lUM6k_IAR_E16PYu33XEkc'

DATABASE = 'fb_scores.db'
LOC_KEYS_TABLE = 'Loc_Keys'
SCORES_TABLE = 'Scores'
NEW_TABLE = 'Game_Locations'
BATCH_SIZE = 25  # Limit to 25 rows per run


def setup_database():
    """Ensure the new table exists."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create new table for game locations
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {NEW_TABLE} (
            game_num INTEGER PRIMARY KEY,
            date_id INTEGER,
            latitude REAL,
            longitude REAL
        )
    ''')
    print(f"'{NEW_TABLE}' table is ready.")

    conn.commit()
    conn.close()


def get_coordinates(city_name):
    """Fetch coordinates for a city using Google Places API."""
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': city_name,
        'inputtype': 'textquery',
        'fields': 'geometry',
        'key': API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] == 'OK' and data['candidates']:
            location = data['candidates'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Error fetching data for '{city_name}': {data.get('status', 'No status')}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Request exception for '{city_name}': {e}")
        return None, None


def process_game_locations():
    """Create game locations with latitude and longitude, processing in batches."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch data from Scores and Loc_Keys tables, limiting to BATCH_SIZE (25)
    cursor.execute(f'''
        SELECT s.game_num, s.date, l.location
        FROM {SCORES_TABLE} s
        JOIN {LOC_KEYS_TABLE} l ON s.location = l.id
        WHERE s.game_num NOT IN (SELECT game_num FROM {NEW_TABLE})
        LIMIT {BATCH_SIZE}
    ''')
    games = cursor.fetchall()

    if not games:
        print("No new game data to process.")
        conn.close()
        return

    for game_num, date_id, city_name in games:
        print(f"Fetching coordinates for '{city_name}'...")
        latitude, longitude = get_coordinates(city_name)

        if latitude is not None and longitude is not None:
            # Insert data into the new table
            cursor.execute(f'''
                INSERT OR REPLACE INTO {NEW_TABLE} (game_num, date_id, latitude, longitude)
                VALUES (?, ?, ?, ?)
            ''', (game_num, date_id, latitude, longitude))
            print(f"Stored game {game_num} with coordinates ({latitude}, {longitude})\n")
        else:
            print(f"Failed to get coordinates for '{city_name}'.\n")

    conn.commit()
    print(f"Processed {len(games)} game locations.")
    conn.close()


def main():
    """Main entry point."""
    setup_database()
    process_game_locations()


if __name__ == "__main__":
    main()
