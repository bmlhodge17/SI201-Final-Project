#calculations and visualizations
import sqlite3
import os
import matplotlib.pyplot as plt


# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "SQL_Data_base.db")

# Get connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    return conn, cur


# Bri CALCULATION 1: Networks per country
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

# #BRI's graphs
# Function to plot the top countries
def plot_networks(data, top_n = 15):
    # Separate into countries and counts
    countries = [row[0] for row in data[:top_n]]
    counts = [row[1] for row in data[:top_n]]
    
    # Create bar chart
    plt.figure(figsize = (12,6))
    plt.bar(countries, counts, color = 'skyblue')
    plt.xticks(rotation = 45, ha = 'right')
    plt.title(f"Top {top_n} Countries by Number of CityBike Networks")
    plt.ylabel("Number of Networks")
    plt.tight_layout()
    plt.show()

#jasmines calculation
# Calculate Average food from sql data base for each city
import sqlite3
import matplotlib.pyplot as plt

def calculate_average_food_scores():
    conn = sqlite3.connect("SQL_Data_base.db")
    cur = conn.cursor()
    
    cur.execute("""
        SELECT city_name,
               (COALESCE(inexpensive_meal, 0) +
                COALESCE(meal_for_two, 0) +
                COALESCE(mcdonalds_meal, 0) +
                COALESCE(domestic_beer, 0) +
                COALESCE(imported_beer, 0) +
                COALESCE(cappuccino, 0) +
                COALESCE(coke, 0)
               ) * 1.0 /
               ((inexpensive_meal IS NOT NULL) +
                (meal_for_two IS NOT NULL) +
                (mcdonalds_meal IS NOT NULL) +
                (domestic_beer IS NOT NULL) +
                (imported_beer IS NOT NULL) +
                (cappuccino IS NOT NULL) +
                (coke IS NOT NULL))
        FROM city_food_costs
    """)
    
    rows = cur.fetchall()
    conn.close()
    
    # Convert scores to float
    result = [(city, float(score)) for city, score in rows if score is not None]
    return result

def plot_scatter_food_scores():
    import matplotlib.pyplot as plt

    data = calculate_average_food_scores()

    cities = []
    scores = []

    for row in data:
        city, score = row
        if score is not None:
            cities.append(city)
            scores.append(score)

    plt.figure(figsize=(14,6))
    plt.scatter(cities, scores)
    plt.xticks(rotation=90)
    plt.xlabel("City")
    plt.ylabel("Average Food Score")
    plt.title("Scatter Plot of Average Food Scores by City")
    plt.tight_layout()
    plt.show()




def main():
    #Bri calculation call
    #data = networks_per_country()
    #plot_networks(data, top_n = 15)
    # Print top 15 for quick check
    # for row in data[:15]:
    #     print(row)
    
    # Plot top 15
    #data = calculate_average_food_scores()
    #data = calculate_average_food_scores()
    # for d in data:
    #     print(d)

    #plot top 15
    # Jasmine calculation call
    plot_scatter_food_scores()    #calculate_average_food_scores()
    # Asiah calculation call
    
    
if __name__ == "__main__":
    main()


