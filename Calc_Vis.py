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


#jasmines calculation
# Calculate Average food from sql data base for each city



def calculate_average_food_scores(db_path="SQL_Data_base.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Select the fields you want to average
    cur.execute("""
        SELECT city_name, inexpensive_meal, meal_for_two, mcdonalds_meal,
               domestic_beer, imported_beer, cappuccino, coke
        FROM city_food_costs
    """)
#collects the results in a new list 
    results = []
    rows = cur.fetchall()

    for row in rows:
        city_name = row[0]

        # Extract all the cost values as a list of floats
        costs = [value for value in row[1:] if value is not None]

        # Safeguard if a city has no valid numbers
        if len(costs) == 0:
            avg_score = None
        else:
            avg_score = round(sum(costs) / len(costs))

        results.append((city_name, avg_score))

    conn.close()
    return results



def main():
    #bri calculation call in main
    data = networks_per_country()
    for row in data[:15]:
        print(row)

    #asiah calculation call


    #jasmine calculation call
    data = calculate_average_food_scores()
    for row in data:
        print(row)


if __name__ == "__main__":
    main()

