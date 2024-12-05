import os
import requests
import sqlite3

API_KEY = 'AIzaSyA1lp0cMVLR6lUM6k_IAR_E16PYu33XEkc'

DATABASE = 'fb_scores.db'
TABLE_NAME = 'Loc_Keys'

#hello

def setup_database():
    """Add latitude and longitude columns to Loc_Keys table if not already present."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Attempt to add 'latitude' column
    try:
        cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN latitude REAL")
        print(f"Added 'latitude' column to '{TABLE_NAME}' table.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print(f"'latitude' column already exists in '{TABLE_NAME}' table.")
        else:
            print(f"Error adding 'latitude' column: {e}")

    # Attempt to add 'longitude' column
    try:
        cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN longitude REAL")
        print(f"Added 'longitude' column to '{TABLE_NAME}' table.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print(f"'longitude' column already exists in '{TABLE_NAME}' table.")
        else:
            print(f"Error adding 'longitude' column: {e}")

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


def update_coordinates(city_id, latitude, longitude):
    """Update latitude and longitude for a city in the Loc_Keys table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'''
        UPDATE {TABLE_NAME}
        SET latitude = ?, longitude = ?
        WHERE id = ?
    ''', (latitude, longitude, city_id))

    conn.commit()
    conn.close()


def process_cities():
    """Fetch and update coordinates for cities without latitude/longitude."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch cities without coordinates
    cursor.execute(f'''
        SELECT id, location FROM {TABLE_NAME}
        WHERE latitude IS NULL OR longitude IS NULL
    ''')
    cities = cursor.fetchall()
    conn.close()

    if not cities:
        print("All cities already have coordinates.")
        return

    print(f"Processing {len(cities)} cities...")

    for city_id, city_name in cities:
        print(f"Fetching coordinates for '{city_name}'...")
        latitude, longitude = get_coordinates(city_name)

        if latitude is not None and longitude is not None:
            update_coordinates(city_id, latitude, longitude)
            print(f"Stored '{city_name}' with coordinates ({latitude}, {longitude})\n")
        else:
            print(f"Failed to get coordinates for '{city_name}'.\n")


def main():
    """Main entry point."""
    setup_database()
    process_cities()


if __name__ == "__main__":
    main()
