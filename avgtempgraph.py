import sqlite3
import matplotlib.pyplot as plt
import os

def setup_db_connection(db_name):
    """Establish a connection to the SQLite database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def get_avg_temperatures(cur):
    """Fetch average temperatures for each location."""
    query = '''
    SELECT l.location, AVG(w.temperature)
    FROM Weather w
    JOIN Game_Locations g ON w.game_id = g.game_num
    JOIN Scores s ON s.game_num = g.game_num
    JOIN Loc_Keys l ON s.location = l.id
    GROUP BY l.location
    ORDER BY AVG(w.temperature) DESC;
    '''
    cur.execute(query)
    return cur.fetchall()

def plot_avg_temperatures(data):
    """Plot average temperatures for each location."""
    locations = [row[0] for row in data]
    temperatures = [row[1] for row in data]

    plt.figure(figsize=(12, 6))
    plt.barh(locations, temperatures)
    plt.xlabel('Average Temperature (°F)')
    plt.ylabel('Location')
    plt.title('Average Temperature for Each Location')
    plt.tight_layout()
    plt.show()

def main():
    cur, conn = setup_db_connection("fb_scores.db")
    data = get_avg_temperatures(cur)
    if data:
        plot_avg_temperatures(data)
    else:
        print("No data found.")
    conn.close()

if __name__ == "__main__":
    main()
