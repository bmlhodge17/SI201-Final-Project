#calculations and visualizations
import sqlite3
import os
import matplotlib.pyplot as plt
import random


# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "JAB_Database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur



# Bri CALCULATION 1: Networks per country
def connect_to_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur

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

def plot_join_cost_and_gasoline(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT cj.city_name, cj.monthly_salary, cj.gasoline_price
        FROM joined_table cj
        WHERE cj.monthly_salary IS NOT NULL AND cj.gasoline_price IS NOT NULL;
    """)

    rows = cur.fetchall()

    if not rows:
        print("no data in joined_table to plot")
        return

    cities = [row[0] for row in rows]
    salaries = [row[1] for row in rows]
    gasoline_prices = [row[2] for row in rows]

    plt.figure(figsize=(14, 7))
    plt.scatter(gasoline_prices, salaries)

    for i, city in enumerate(cities):
        plt.annotate(city, (gasoline_prices[i], salaries[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)

    plt.xlabel("Gasoline Price per Liter (USD)")
    plt.ylabel("Average Monthly Salary (USD)")
    plt.title("Monthly Salary vs Gasoline Price per Liter")
    plt.tight_layout()
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


# uv index histogram with colored bins
def plot_uv_index_histogram():
    conn, cur = connect_to_database()

    # get uv index values from weather table
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

    # uv index bins grouped by 2
    bins = [0, 2, 4, 6, 8, 10, 12]

    plt.figure(figsize=(8, 5))

    # create histogram and capture bars
    counts, bin_edges, patches = plt.hist(
        uv_values,
        bins=bins,
        edgecolor="black"
    )

    # colors for each uv range
    colors = [
        "#7FB3D5",  # low
        "#76D7C4",  # moderate
        "#F7DC6F",  # high
        "#F5B041",  # very high
        "#EB984E",  # extreme
        "#E74C3C"   # extreme+
    ]

    # apply colors to each bin
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)

    plt.xlim(0, 12)
    plt.xlabel("uv index")
    plt.ylabel("number of cities")
    plt.title("distribution of uv index across cities (grouped by 2)")
    plt.tight_layout()
    plt.show()

# weather description dot plot
#with city labels

def plot_weather_description_dotplot():
    conn, cur = connect_to_database()

    # get city names and weather descriptions
    cur.execute("""
        SELECT city_name, weather_description
        FROM weather
        WHERE weather_description IS NOT NULL;
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("no weather description data to plot")
        return

    # group cities by weather description
    grouped = {}
    for city, desc in rows:
        grouped.setdefault(desc, []).append(city)

    x_vals = []
    y_vals = []
    labels = []

    # build dot positions
    for desc, cities in grouped.items():
        for i, city in enumerate(cities):
            x_vals.append(desc)
            y_vals.append(i + 1)
            labels.append(city)

    plt.figure(figsize=(16, 7))
    plt.scatter(x_vals, y_vals)

    # add city labels next to each dot
    for x, y, label in zip(x_vals, y_vals, labels):
        plt.text(
            x,
            y + 0.05,
            label,
            fontsize=8,
            rotation=30,
            ha="left"
        )

    plt.xlabel("weather description")
    plt.ylabel("number of cities")
    plt.title("dot plot of weather descriptions labeled by city")
    plt.xticks(rotation=45, ha="right")
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
    conn = sqlite3.connect(DB_PATH)
    # Bri calculation call
    countries, counts = networks_per_country()

    # Plot top 15, call networks plot
    plot_networks(countries, counts, top_n=15)
    
    #jasmines calculations
    #join table plot call
    plot_join_cost_and_gasoline(conn)
   
    average_salary_first_25()

    #Asiahs calls
    plot_uv_index_histogram()
    plot_weather_description_dotplot()
    plot_top_10_hottest()
    plot_top_10_coldest()
 


if __name__ == "__main__":
    main()
