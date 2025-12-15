#calculations and visualizations
import sqlite3
import os
import matplotlib.pyplot as plt
import random


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
    #separate into countries and counts
    countries = [row[0] for row in data[:top_n]]
    counts = [row[1] for row in data[:top_n]]
    
    #create bar chart
    plt.figure(figsize = (12,6))
    plt.bar(countries, counts, color = 'skyblue')
    plt.xticks(rotation = 45, ha = 'right')
    plt.title(f"Top {top_n} Countries by Number of CityBike Networks")
    plt.ylabel("Number of Networks")
    plt.tight_layout()
    plt.show()
#jasmines calculation
# Calculate Average food from sql data base for each city
import matplotlib.pyplot as plt

# def calculate_average_food_scores():
#     conn = sqlite3.connect("SQL_Data_base.db")
#     cur = conn.cursor()
    
#     cur.execute("""
#         SELECT city_name,
#                (COALESCE(inexpensive_meal, 0) +
#                 COALESCE(meal_for_two, 0) +
#                 COALESCE(mcdonalds_meal, 0) +
#                 COALESCE(domestic_beer, 0) +
#                 COALESCE(imported_beer, 0) +
#                 COALESCE(cappuccino, 0) +
#                 COALESCE(coke, 0)
#                ) * 1.0 /
#                ((inexpensive_meal IS NOT NULL) +
#                 (meal_for_two IS NOT NULL) +
#                 (mcdonalds_meal IS NOT NULL) +
#                 (domestic_beer IS NOT NULL) +
#                 (imported_beer IS NOT NULL) +
#                 (cappuccino IS NOT NULL) +
#                 (coke IS NOT NULL))
#         FROM city_food_costs
#     """)
    
#     rows = cur.fetchall()
#     conn.close()
    
    # Convert scores to float
#     result = [(city, float(score)) for city, score in rows if score is not None]
#     return result

# def plot_scatter_food_scores():
#     import matplotlib.pyplot as plt

#     data = calculate_average_food_scores()

#     cities = []
#     scores = []

#     for row in data:
#         city, score = row
#         if score is not None:
#             cities.append(city)
#             scores.append(score)

#     plt.figure(figsize=(14,6))
#     plt.scatter(cities, scores)
#     plt.xticks(rotation=90)
#     plt.xlabel("City")
#     plt.ylabel("Average Food Score")
#     plt.title("Scatter Plot of Average Food Scores by City")
#     plt.tight_layout()
#     plt.show()




# short main removed; consolidated in the unified main below

# Asiah calculation call

#histogram of uv index

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

def plot_weather_description_dotplot():
    conn, cur = connect_to_database()

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

    # unique descriptions for y-axis
    unique_desc = list(set(descriptions))
    y_map = {desc: i for i, desc in enumerate(unique_desc)}

    x_vals = []
    y_vals = []

    for desc in descriptions:
        x_vals.append(random.uniform(0, 1))
        y_vals.append(y_map[desc])

    plt.figure(figsize=(10, 6))
    plt.scatter(x_vals, y_vals, alpha=0.6)
    plt.yticks(range(len(unique_desc)), unique_desc)
    plt.xlabel("random spread")
    plt.ylabel("weather description")
    plt.title("dot plot of weather descriptions")
    plt.tight_layout()
    plt.show()
    
def main():
    # Bri calculation call
    data = networks_per_country()
    
    # Print top 15 for quick check
    for row in data[:15]:
        print(row)
    
    # Plot top 15, call networks plot
    plot_networks(data, top_n = 15)

    # Asiah calculation call
    # uv index histogram
    plot_uv_index_histogram()
    # weather description dotplot
    plot_weather_description_dotplot()

    # jasmine calculation call
    # (add Jasmine's calls/plots here if needed)
    # weather description dotplot
    plot_weather_description_dotplot()
    plot_uv_index_histogram()

    # jasmine calculation call
    # (add Jasmine's calls/plots here if needed)
def get_top_15_salaries(db_path="AB_SQL_Data_base.db"):


    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Get city + salary, ignore NULLs
    cur.execute("""
        SELECT city_name, monthly_salary
        FROM cost_index
        WHERE monthly_salary IS NOT NULL
    """)

    rows = cur.fetchall()
    conn.close()

    # Convert salary strings -> float
    cleaned = []
    for city, salary in rows:
        try:
            salary_float = float(salary)
            cleaned.append((city, salary_float))
        except:
            continue  # skip corrupted values

    # Sort by salary descending and take top 15
    top15 = sorted(cleaned, key=lambda x: x[1], reverse=True)[:15]
    cities = [item[0] for item in top15]
    salaries = [item[1] for item in top15]

    #plot
    plt.figure(figsize=(14, 7))
    plt.bar(cities, salaries)
    plt.title("Top 15 Cities by Monthly Salary index")
    plt.xlabel("City")
    plt.ylabel("Average Monthly Salary (USD)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
