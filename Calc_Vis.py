#calculations and visualizations
import sqlite3
import os

# Path to the SQLite database, same used in data base py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "SQL_Data_base.db")

#get connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur


# Bri CALCULATION 1 for Citybikes API
# Calculate Average free bikes per city at their stations

def calc_average_free_bikes():
    conn, cur = get_connection()

    query = """
        SELECT 
            c.city_name,
            AVG(s.free_bikes) AS avg_free_bikes
        FROM stations s
        JOIN networks n ON s.network_id = n.network_id
        JOIN cities c ON n.city_id = c.city_id
        GROUP BY c.city_id
        ORDER BY avg_free_bikes DESC;
    """

    cur.execute(query)
    results = cur.fetchall()
    conn.close()

    return results




def main():
    #bri calculation call in main
    results = calc_average_free_bikes()

    print("Average Number of Free Bikes per City:")
    
    for city, avg_bikes in results:
        print(f"{city}: {avg_bikes:.2f}")

    #asiah calculation call


    #jasmine calculation call



if __name__ == "__main__":
    main()

