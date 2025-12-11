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


#function to plot the top countries
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



# short main removed; consolidated in the unified main below

# Asiah calculation call
#top 10 cities with highest temperature
#top 10 with lowest temperature
#top 10 with highest humidity
#top 10 with lowest humidity
#pie chart of wind directions
#pie chart of uv index

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


# this gets the hottest or coldest cities by joining weather and city name tables
def get_top_cities_by_temp(highest=True, limit=10):
    order = "desc" if highest else "asc"
    query = f"""
        select wc.city_name, cw.temperature
        from current_weather cw
        join weather_cities wc on cw.city_id = wc.city_id
        where cw.temperature is not null
        order by cw.temperature {order}
        limit ?;
    """
    return run_query(query, (limit,))


# this makes a bar graph for any (city, value) data
def plot_top_cities_bar(data, metric_label, title):
    cities = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.bar(cities, values)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel(metric_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# this gets the cities with the highest or lowest humidity
def get_top_cities_by_humidity(highest=True, limit=10):
    order = "desc" if highest else "asc"
    query = f"""
        select wc.city_name, cw.humidity
        from current_weather cw
        join weather_cities wc on cw.city_id = wc.city_id
        where cw.humidity is not null
        order by cw.humidity {order}
        limit ?;
    """
    return run_query(query, (limit,))


# this gets how many cities have each wind direction
def get_wind_direction_counts():
    query = """
        select cw.wind_dir, count(*) as count_dir
        from current_weather cw
        where cw.wind_dir is not null
        group by cw.wind_dir
        order by count_dir desc;
    """
    return run_query(query)


# this gets how many cities have each uv index value
def get_uv_index_counts():
    query = """
        select cw.uv_index, count(*) as count_uv
        from current_weather cw
        where cw.uv_index is not null
        group by cw.uv_index
        order by cw.uv_index;
    """
    return run_query(query)


# this makes pie charts for wind direction and uv index
def plot_pie_from_counts(data, title):
    if not data:
        print("no data for pie chart:", title)
        return

    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title(title)
    plt.tight_layout()
    plt.show()

def main():
    # bri calculation call
    data = networks_per_country()
    for row in data[:15]:
        print(row)
    plot_networks(data, top_n=15)

    # asiahs calculations

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

    # pie chart of wind directions
    wind_data = get_wind_direction_counts()
    plot_pie_from_counts(wind_data, "wind direction distribution")

    # pie chart of uv index
    uv_data = get_uv_index_counts()
    plot_pie_from_counts(uv_data, "uv index distribution")

# Jasmine calculation call

if __name__ == "__main__":
    main()
