#calculations and visualizations
import sqlite3
import os
import matplotlib.pyplot as plt
import random


# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "JAB_Database.db")

# Get connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    return conn, cur


# Bri CALCULATION 1: Networks per country
from SQL_Data_base import connect_to_database

def networks_per_country():
    """
    Returns two lists:
    - countries
    - network counts
    sorted from most to least networks
    """
    conn, cur = connect_to_database()

    cur.execute("""
        SELECT country, COUNT(*) AS num_networks
        FROM cities
        WHERE country IS NOT NULL
        GROUP BY country
        ORDER BY num_networks DESC;
    """)

    rows = cur.fetchall()
    conn.close()

    # separate into two lists (same pattern as other calculations)
    countries = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    return countries, counts


# Function to plot the top countries
def plot_networks(countries, counts, top_n=15):
    countries = countries[:top_n]
    counts = counts[:top_n]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(countries, counts)
    for bar in bars:
        bar.set_color("green")

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Country")
    plt.ylabel("Number of Networks")
    plt.title(f"Top {top_n} Countries by Number of CityBike Networks")
    plt.tight_layout()
    plt.show()


#jasmines calculation
# joined table calculation 


def plot_join_table(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Select data from join table
    cur.execute("""
        SELECT monthly_salary, gasoline_price
        FROM joined_table
        WHERE monthly_salary IS NOT NULL
          AND gasoline_price IS NOT NULL;
    """)

    rows = cur.fetchall()

    if not rows:
        print("No data available for scatter plot.")
        return

    salaries = [row[0] for row in rows]
    gas_prices = [row[1] for row in rows]

    # Create scatter plot
    plt.figure()
    plt.scatter(salaries, gas_prices)
    plt.xlabel("Average Monthly Salary")
    plt.ylabel("Gasoline Price (per liter)")
    plt.title("Monthly Salary vs Gasoline Price by City")
    plt.show()

#calculating the average salary in the first 25 cities in the cost index table
def average_salary_first_25():
    conn, cur = get_connection()
    query = """
        SELECT AVG(monthly_salary)
        FROM cost_index
        WHERE city_id IN (
            SELECT city_id
            FROM cost_index
            ORDER BY city_id
            LIMIT 25
        )
        AND monthly_salary IS NOT NULL;
    """
    cur.execute(query)
    avg_salary = cur.fetchone()[0]
    conn.close()
    print(avg_salary)

#asiahs visualizations
# this helper runs any sql query so i don’t have to repeat the connection stuff
def run_query(query, params=None):
    conn, cur = connect_to_database()
    if params is None:
        cur.execute(query)
    else:
        cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "JAB_Database.db")

# connect to database
def connect_to_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur


# uv index histogram
def plot_uv_index_histogram():
    conn, cur = connect_to_database()

    # get uv index values
    cur.execute("""
        SELECT uv_index
        FROM weather
        WHERE uv_index IS NOT NULL;
    """)

    rows = cur.fetchall()
    conn.close()

    uv_values = [row[0] for row in rows]

    if not uv_values:
        print("no uv index data to plot")
        return

    # make histogram
    plt.figure(figsize=(8, 5))
    plt.hist(uv_values, bins=10)
    plt.xlabel("uv index")
    plt.ylabel("number of cities")
    plt.title("distribution of uv index across cities")
    plt.tight_layout()
    plt.show()

# weather description dot plot

def plot_weather_description_dotplot():
    conn, cur = connect_to_database()

    # get weather descriptions
    cur.execute("""
        SELECT weather_description
        FROM weather
        WHERE weather_description IS NOT NULL;
    """)

    rows = cur.fetchall()
    conn.close()

    descriptions = [row[0] for row in rows]

    if not descriptions:
        print("no weather description data to plot")
        return

    # count how many times each description appears
    counts = {}
    for desc in descriptions:
        counts[desc] = counts.get(desc, 0) + 1

    unique_desc = list(counts.keys())
    y_map = {desc: i for i, desc in enumerate(unique_desc)}

    x_vals = []
    y_vals = []

    # create dots based on frequency
    for desc, count in counts.items():
        for i in range(count):
            x_vals.append(i + 1)  # count-based x-axis
            y_vals.append(y_map[desc])

    plt.figure(figsize=(12, 6))
    plt.scatter(x_vals, y_vals)
    plt.yticks(range(len(unique_desc)), unique_desc)
    plt.xlabel("number of cities")
    plt.ylabel("weather description")
    plt.title("dot plot of weather descriptions by frequency")
    plt.tight_layout()
    plt.show()


def plot_top_10_hottest():
    conn, cur = connect_to_database()

    cur.execute("""
        SELECT city_name, temperature
        FROM weather
        WHERE temperature IS NOT NULL
        ORDER BY temperature DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("no temperature data for hottest cities")
        return

    cities = [row[0] for row in rows]
    temps = [row[1] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.barh(cities, temps)
    plt.xlabel("temperature (celsius)")
    plt.ylabel("city")
    plt.title("top 10 hottest cities (celsius)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


# top 10 lowest temperatures 
def plot_top_10_coldest():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT city_name, temperature
        FROM weather
        WHERE temperature IS NOT NULL
        ORDER BY temperature ASC
        LIMIT 10;
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("no temperature data for coldest cities")
        return

    cities = [row[0] for row in rows]
    temps = [row[1] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.barh(cities, temps)
    plt.xlabel("temperature (celsius)")
    plt.ylabel("city")
    plt.title("top 10 coldest cities (celsius)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


    #

def main():
    # Bri calculation call
    data = networks_per_country()
    
    # Print top 15 for quick check
    for row in data[:15]:
        print(row)
    
    # Plot top 15, call networks plot
    plot_networks(data, top_n = 15)

    # Asiah calculation call

    # top 10 hottest cities
    hottest = get_top_cities_by_temp(highest=True, limit=10)
    plot_top_cities_bar(hottest, "temperature", "top 10 hottest cities")

    # top 10 coldest cities
    coldest = get_top_cities_by_temp(highest=False, limit=10)
    plot_top_cities_bar(coldest, "temperature", "top 10 coldest cities")

    # top 10 most humid cities
    most_humid = get_top_cities_by_humidity(highest=True, limit=10)
    plot_top_cities_bar(most_humid, "humidity", "top 10 most humid cities")

    # top 10 least humid cities
    least_humid = get_top_cities_by_humidity(highest=False, limit=10)
    plot_top_cities_bar(least_humid, "humidity", "top 10 least humid cities")

    # wind direction pie chart
    wind_data = get_wind_direction_counts()
    plot_pie_from_counts(wind_data, "wind direction distribution")

    # uv index pie chart
    uv_data = get_uv_index_counts()
    plot_pie_from_counts(uv_data, "uv index distribution")
#----Jasmines code ----
    #join table plot call
    #plot_join_table(get_connection()[0])
    #average salary calculation call
    get_connection()
    countries, counts = networks_per_country()
    plot_networks(countries, counts, top_n=15)

    average_salary_first_25()
    plot_uv_index_histogram()
    plot_weather_description_dotplot()
    plot_top_10_hottest()
    plot_top_10_coldest()
 


if __name__ == "__main__":
    main()
