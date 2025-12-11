import unittest
import sqlite3
import os
import json
import requests


#Bri's tables
#SQL_Data_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SQL_Data_base.db")
#.py file creates our .db file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_Data_base = os.path.join(BASE_DIR, "AB_SQL_Data_base.db")

def connect_to_database():
    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    return conn, cur


def create_citybike_tables():
    conn, cur = connect_to_database()

    # ---------- CREATE TABLES ----------
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE,
            country TEXT,
            latitude REAL,
            longitude REAL
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS networks (
            network_id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_network_id TEXT UNIQUE,
            network_name TEXT,
            city_id INTEGER,
            FOREIGN KEY(city_id) REFERENCES cities(city_id)
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            station_id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_station_id TEXT UNIQUE,
            station_name TEXT,
            free_bikes INTEGER,
            empty_slots INTEGER,
            latitude REAL,
            longitude REAL,
            timestamp TEXT,
            network_id INTEGER,
            city_id INTEGER,
            FOREIGN KEY(network_id) REFERENCES networks(network_id),
            FOREIGN KEY(city_id) REFERENCES cities(city_id)
        );
    ''')

    conn.commit()

    # ---------- LOAD NETWORK LIST ----------
    print("Loading network list...")
    url = "https://api.citybik.es/v2/networks"
    networks = requests.get(url).json().get("networks", [])

    # ---------- INSERT CITIES + NETWORKS ----------
    for n in networks:

        api_id = n.get("id")
        network_name = n.get("name")
        loc = n.get("location", {})

        city = loc.get("city")
        country = loc.get("country")
        lat = loc.get("latitude")
        lon = loc.get("longitude")

        # Insert city
        cur.execute("""
            INSERT OR IGNORE INTO cities (city_name, country, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (city, country, lat, lon))

        # get city_id
        cur.execute("SELECT city_id FROM cities WHERE city_name=?", (city,))
        city_fk = cur.fetchone()[0]

        # Insert network
        cur.execute("""
            INSERT OR IGNORE INTO networks (api_network_id, network_name, city_id)
            VALUES (?, ?, ?)
        """, (api_id, network_name, city_fk))

    conn.commit()

    # ---------- INSERT STATIONS ----------
    print("Loading station data from detail endpoints...")

    for n in networks:
        api_id = n.get("id")

        # Get foreign keys
        cur.execute("SELECT network_id, city_id FROM networks WHERE api_network_id=?", (api_id,))
        row = cur.fetchone()
        if not row:
            continue

        network_fk, city_fk = row

        detail_url = f"https://api.citybik.es/v2/networks/{api_id}"

        try:
            detail_data = requests.get(detail_url).json()
            stations = detail_data.get("network", {}).get("stations", [])

        except Exception as e:
            print("Error fetching stations for", api_id, e)
            continue

        for s in stations:
            cur.execute("""
                INSERT OR IGNORE INTO stations (
                    api_station_id, station_name, free_bikes, empty_slots,
                    latitude, longitude, timestamp, network_id, city_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s.get("id"),
                s.get("name"),
                s.get("free_bikes"),
                s.get("empty_slots"),
                s.get("latitude"),
                s.get("longitude"),
                s.get("timestamp"),
                network_fk,
                city_fk
            ))

    conn.commit()
    conn.close()

    print("CityBikes data successfully loaded!")



#Asiah's tables
def create_weather_tables():
    #with open("weather_100_cities.json", "r") as f:
        #data = json.load(f)
    json_path = os.path.join(BASE_DIR, "weather_100_cities.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    cities = data["cities"]


    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()



    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_cities (
        city_id INTEGER PRIMARY KEY,
        city_name TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        type TEXT,
        query TEXT,
        language TEXT,
        unit TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id),
        UNIQUE (city_id, type, query, language, unit)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        name TEXT,
        country TEXT,
        region TEXT,
        lat REAL,
        lon REAL,
        timezone_id TEXT,
        localtime TEXT,
        localtime_epoch INTEGER,
        utc_offset TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS current_weather (
        current_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        observation_time TEXT,
        temperature REAL,
        weather_code INTEGER,
        wind_speed REAL,
        wind_degree REAL,
        wind_dir TEXT,
        pressure REAL,
        precip REAL,
        humidity REAL,
        cloudcover REAL,
        feelslike REAL,
        uv_index REAL,
        visibility REAL,
        is_day TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_icons (
        icon_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        icon_url TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id, icon_url)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_descriptions (
        description_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        description TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id, description)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS astro (
        astro_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        sunrise TEXT,
        sunset TEXT,
        moonrise TEXT,
        moonset TEXT,
        moon_phase TEXT,
        moon_illumination INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS air_quality (
        aq_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        co REAL,
        no2 REAL,
        o3 REAL,
        so2 REAL,
        pm2_5 REAL,
        pm10 REAL,
        us_epa_index INTEGER,
        gb_defra_index INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_urls (
        url_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER,
        weatherstack_url TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id), UNIQUE (city_id)
    );
    """)

    conn.commit()



    for c in cities:
        city_id = c["city_id"]
        city_name = c["city_name"]

        #insert into cities
        cur.execute("""
            INSERT OR REPLACE INTO weather_cities (city_id, city_name)
            VALUES (?, ?)
        """, (city_id, city_name))

        # request
        req = c.get("request", {})
        cur.execute("""
            INSERT INTO requests (city_id, type, query, language, unit)
            VALUES (?, ?, ?, ?, ?)
        """, (
            city_id,
            req.get("type"),
            req.get("query"),
            req.get("language"),
            req.get("unit")
        ))

        #location
        loc = c.get("location", {})
        cur.execute("""
            INSERT OR REPLACE INTO locations (
                city_id, name, country, region, lat, lon,
                timezone_id, localtime, localtime_epoch, utc_offset
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            city_id,
            loc.get("name"),
            loc.get("country"),
            loc.get("region"),
            loc.get("lat"),
            loc.get("lon"),
            loc.get("timezone_id"),
            loc.get("localtime"),
            loc.get("localtime_epoch"),
            loc.get("utc_offset")
        ))

        #current weather
        cur_weather = c.get("current", {})
        cur.execute("""
            INSERT OR REPLACE INTO current_weather (
                city_id, observation_time, temperature, weather_code,
                wind_speed, wind_degree, wind_dir, pressure, precip,
                humidity, cloudcover, feelslike, uv_index, visibility, is_day
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            city_id,
            cur_weather.get("observation_time"),
            cur_weather.get("temperature") or cur_weather.get("temparature"),
            cur_weather.get("weather_code"),
            cur_weather.get("wind_speed"),
            cur_weather.get("wind_degree"),
            cur_weather.get("wind_dir"),
            cur_weather.get("pressure"),
            cur_weather.get("precip"),
            cur_weather.get("humidity"),
            cur_weather.get("cloudcover"),
            cur_weather.get("feelslike"),
            cur_weather.get("uv_index"),
            cur_weather.get("visibility"),
            cur_weather.get("is_day")
        ))

        #icons
        for icon in cur_weather.get("weather_icons", []):
            cur.execute("INSERT OR IGNORE INTO weather_icons (city_id, icon_url) VALUES (?, ?)",
                        (city_id, icon))

        # descriptions
        for desc in cur_weather.get("weather_descriptions", []):
            cur.execute("INSERT OR IGNORE INTO weather_descriptions (city_id, description) VALUES (?, ?)",
                        (city_id, desc))

        # astro
        astro = cur_weather.get("astro", {})
        if astro:
            cur.execute("""
                INSERT OR IGNORE INTO astro (
                    city_id, sunrise, sunset, moonrise, moonset,
                    moon_phase, moon_illumination
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                city_id,
                astro.get("sunrise"),
                astro.get("sunset"),
                astro.get("moonrise"),
                astro.get("moonset"),
                astro.get("moon_phase"),
                astro.get("moon_illumination")
            ))

        # air quality
        aq = cur_weather.get("air_quality", {})
        if aq:
            cur.execute("""
                INSERT OR IGNORE INTO air_quality (
                    city_id, co, no2, o3, so2, pm2_5, pm10,
                    us_epa_index, gb_defra_index
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                city_id,
                aq.get("co"),
                aq.get("no2"),
                aq.get("o3"),
                aq.get("so2"),
                aq.get("pm2_5"),
                aq.get("pm10"),
                aq.get("us-epa-index"),
                aq.get("gb-defra-index")
            ))

        #url
        cur.execute("""
            INSERT OR REPLACE INTO api_urls (city_id, weatherstack_url)
            VALUES (?, ?)
        """, (city_id, c.get("weatherstack_url")))

    #save
    conn.commit()
    conn.close()

# print("Database created")

#kaggle function 

#city id, city name, and food 

import sqlite3
import json

SQL_Data_base = "SQL_Data_base.db"

def cost_index_table():
    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    # Create table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cost_index (
            city_id INTEGER PRIMARY KEY,
            city_name TEXT UNIQUE,
            cost_index REAL,
            monthly_salary REAL
        );
    ''')

    conn.commit()

    # Load data from JSON file
    with open("cities_living_cost.json", "r") as f:
        data = json.load(f)  # load JSON properly

    for row in data:
        city_id = int(row.get("", 0))  # the "" key in your JSON
        city_name = row.get("City", "Unknown")
        cost_index = float(row.get("Cost_index", 0))
        monthly_salary = float(row.get("Average Monthly Net Salary (After Tax)", 0))

        cur.execute('''
            INSERT OR REPLACE INTO cost_index (city_id, city_name, cost_index, monthly_salary)
            VALUES (?, ?, ?, ?)
        ''', (city_id, city_name, cost_index, monthly_salary))

    conn.commit()
    conn.close()

    print("Cost index and salary data successfully loaded!")


def main():
    create_citybike_tables()
    create_weather_tables()
    cost_index_table()

if __name__ == "__main__":
    main()
