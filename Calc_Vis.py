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
# Calculate Average 
from SQL_Data_base import connect_to_database

def networks_per_country():
    """
    Returns a list of (country, count_of_networks)
    sorted by most to least networks.
    """

    conn, cur = connect_to_database()

    query = """
        SELECT country, COUNT(*) as num_networks
        FROM cities
        WHERE country IS NOT NULL
        GROUP BY country
        ORDER BY num_networks DESC;
    """

    cur.execute(query)
    results = cur.fetchall()

    conn.close()
    return results





def main():
    #bri calculation call in main
    data = networks_per_country()
    for row in data[:15]:
        print(row)

    #asiah calculation call


    #jasmine calculation call



if __name__ == "__main__":
    main()

