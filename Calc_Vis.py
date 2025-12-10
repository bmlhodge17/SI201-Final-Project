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



def main():
    # Bri calculation call
    data = networks_per_country()
    
    # Print top 15 for quick check
    for row in data[:15]:
        print(row)
    
    # Plot top 15
    plot_networks(data, top_n = 15)

    # Asiah calculation call
    

    # Jasmine calculation call

if __name__ == "__main__":
    main()


