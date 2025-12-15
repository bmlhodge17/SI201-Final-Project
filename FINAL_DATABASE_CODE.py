import os
import re
import sqlite3
import requests
from datetime import datetime
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "JAB_Database.db")

def canon_city(name: str) -> str:
    """Lowercase, trim and collapse whitespace."""
    if not name:
        return ""
    name = name.strip().lower()
    return re.sub(r"\s+", " ", name)

def init_db(conn: sqlite3.Connection) -> None:
    """Create the `cities` table if it does not exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            city_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name  TEXT UNIQUE NOT NULL,
            country    TEXT,
            latitude   REAL,
            longitude  REAL,
            updated_at TEXT
        );
        """
    )
    conn.commit()

def fetch_networks() -> list[dict]:
    """Return the list of network objects from the public API."""
    url = "https://api.citybik.es/v2/networks"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json().get("networks", [])

def upsert_cities(
    conn: sqlite3.Connection,
    networks: list[dict],
    limit: int = 25
) -> None:
    """
    Insert only new city rows.
    If you later want to *update* existing rows, replace the INSERT statement
    with the ON CONFLICT DO UPDATE version (see the table above).
    """

    insert_sql = """
        INSERT OR IGNORE INTO cities
        (city_name, country, latitude, longitude, updated_at)
        VALUES (?, ?, ?, ?, ?);
    """

    cur = conn.cursor()
    added = 0

    for net in networks:
        if added >= limit:
            break

        loc = net.get("location", {})
        raw_city = loc.get("city")

        if not raw_city:
            continue

        city_norm = canon_city(raw_city)
        country   = loc.get("country")
        lat       = loc.get("latitude")
        lon       = loc.get("longitude")
        ts        = datetime.utcnow().isoformat(timespec="seconds")

        cur.execute(
            insert_sql,
            (city_norm, country, lat, lon, ts)
        )

        # rowcount == 1  a new row was inserted; 0  ignored because it already existed
        if cur.rowcount == 1:
            added += 1

    conn.commit()
    print(f"New rows inserted: {added}")

#JASMINES CODE:
csv_file = 'kaggle data base/cities_living_cost.csv'
json_file = 'cities_living_cost.json'

# Read CSV and convert to a list of dictionaries
def convert_csv_to_json():
    data = []
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(json_file, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


SQL_Data_base = "JAB_Database.db"
def cost_index_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cost_index (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE NOT NULL,
            monthly_salary REAL
        );
    """)
    conn.commit()


#limit to 25 rows:
def upsert_cost_index(
    conn: sqlite3.Connection,
    limit: int = 25
) -> None:

    with open("cities_living_cost.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    insert_sql = """
        INSERT OR IGNORE INTO cost_index
        (city_name, monthly_salary)
        VALUES (?, ?);
    """

    cur = conn.cursor()
    added = 0

    for row in data:
        if added >= limit:
            break

        raw_city = row.get("City")
        salary_raw = row.get("Average Monthly Net Salary (After Tax)")

        if not raw_city:
            continue

        city_norm = canon_city(raw_city)

        try:
            monthly_salary = float(salary_raw) if salary_raw else None
        except ValueError:
            monthly_salary = None

        cur.execute(
            insert_sql,
            (city_norm, monthly_salary)
        )

        if cur.rowcount == 1:
            added += 1

    conn.commit()
    print(f"New rows inserted into cost_index: {added}")

#create gasolien index table
def create_gasoline_index_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gasoline_index (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE NOT NULL,
            gasoline_price REAL
        );
    """)
    conn.commit()


#creating 25 gasoline rows
def upsert_gasoline_index(
    conn: sqlite3.Connection,
    limit: int = 25
) -> None:

    with open("cities_living_cost.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    insert_sql = """
        INSERT OR IGNORE INTO gasoline_index
        (city_name, gasoline_price)
        VALUES (?, ?);
    """

    cur = conn.cursor()
    added = 0

    for row in data:
        if added >= limit:
            break

        raw_city = row.get("City")
        gasoline_raw = row.get("Gasoline (1 liter)")

        if not raw_city:
            continue

        city_norm = canon_city(raw_city)

        try:
            gasoline_price = float(gasoline_raw) if gasoline_raw else None
        except ValueError:
            gasoline_price = None

        cur.execute(
            insert_sql,
            (city_norm, gasoline_price)
        )

        if cur.rowcount == 1:
            added += 1

    conn.commit()
    print(f"New rows inserted into gasoline_index: {added}")




#----JOIN TABLE ----
#joining jazz's salary and bri's city_name tables 
def create_join_table(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Drop first to avoid stale schemas
    cur.execute("DROP TABLE IF EXISTS joined_table")

    cur.execute("""
        CREATE TABLE joined_table AS
        SELECT
            c.city_name,
            c.monthly_salary,
            g.gasoline_price
        FROM cost_index c
        JOIN gasoline_index g
            ON c.city_name = g.city_name;
    """)

    conn.commit()
    print("joined_table created successfully!")



    

  #asiahs weather code:  
API_KEY = "b4e833d38c9ea664b0cd9c76f2c84a6f"


def init_weather_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER UNIQUE NOT NULL,
            city_name TEXT NOT NULL,
            weather_description TEXT,
            uv_index INTEGER,
             temperature REAL,
            updated_at TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(city_id)
        );
        """
    )

    # check existing columns in the weather table
    # this prevents errors if the table was created earlier without city_name
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(weather);")
    columns = [col[1] for col in cur.fetchall()]


    # add uv_index if missing
    if "uv_index" not in columns:
        cur.execute("ALTER TABLE weather ADD COLUMN uv_index REAL;")
    # add temperature if missing

    if "temperature" not in columns:
        cur.execute("ALTER TABLE weather ADD COLUMN temperature REAL;")

    # add city_name column only if it is missing
    if "city_name" not in columns:
        cur.execute("ALTER TABLE weather ADD COLUMN city_name TEXT;")

    conn.commit()



# fetch weather data from weatherstack api
# takes a city name and returns relevant weather info
def get_city_weather(city_name):
    # build request url using api key and city name
    url = (
        f"http://api.weatherstack.com/current"
        f"?access_key={API_KEY}&query={city_name}"
    )

    resp = requests.get(url, timeout=15)
    data = resp.json()

    # default fallback weather data
    weather = {
        "weather_description": "data unavailable",
        "uv_index": None, "temperature": None
    }

    # handle api errors (common on free tier)
    if data.get("success") is False:
        print("WEATHERSTACK ERROR FOR", city_name, data)
        return None

    # sometimes api returns success but no current weather data
    current = data.get("current")
    if not current:
        print("NO CURRENT WEATHER FOR", city_name, data)
        return weather

    # extract first weather description if available
    description = None
    if current.get("weather_descriptions"):
        description = current["weather_descriptions"][0]

    uv_index = current.get("uv_index")
    weather["temperature"] = current.get("temperature")

    return {
        "weather_description": description,
        "uv_index": current.get("uv_index"),  "temperature": current.get("temperature")
    }
def add_uv_index_column(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(weather);")
    columns = [col[1] for col in cur.fetchall()]

    if "uv_index" not in columns:
        cur.execute("ALTER TABLE weather ADD COLUMN uv_index REAL;")

    conn.commit()
    



# pulls city_id and city_name from cities table
# makes api call for each city and inserts weather data into weather table
def populate_weather(conn, limit=25):
    cur = conn.cursor()

    # get city_id and city_name from cities table
    cur.execute(
        """
        SELECT city_id, city_name
        FROM cities
        LIMIT ?
        """,
        (limit,),
    )

    cities = cur.fetchall()
    print("cities available for weather:", len(cities))

    # THIS LOOP MUST BE INSIDE THE FUNCTION
    for city_id, city_name in cities:
        weather = get_city_weather(city_name.title())

        
        cur.execute(
            """
            INSERT OR REPLACE INTO weather
            (city_id, city_name, weather_description, uv_index, temperature, updated_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                city_id,
                city_name,
                weather["weather_description"],
                weather["uv_index"],
                weather["temperature"],
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )

    conn.commit()
    print("weather table populated")


#main function
# runs city setup first, then weather setup
# ensures tables are populated in correct order


def main():
    print("USING DB FILE:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    try:
       
        # bri: cities api
     
        init_db(conn)
        networks = fetch_networks()
        upsert_cities(conn, networks)

        city_count = conn.execute(
            "SELECT COUNT(*) FROM cities;"
        ).fetchone()[0]
        print("CITIES COUNT:", city_count)

       
        # jasmines calls
#creates tables 
        cost_index_table(conn)
        create_gasoline_index_table(conn)
    #  inserts 25 rows each
        upsert_cost_index(conn)

        upsert_gasoline_index(conn)
        
    #join table call 
        create_join_table(conn)

        cost_count = conn.execute(
            "SELECT COUNT(*) FROM cost_index;"
        ).fetchone()[0]
        print("COST INDEX COUNT:", cost_count)

       
        # asiah: weather api
       
        init_weather_table(conn)
        populate_weather(conn)
        add_uv_index_column(conn)

        weather_count = conn.execute(
            "SELECT COUNT(*) FROM weather;"
        ).fetchone()[0]
        print("WEATHER COUNT:", weather_count)

     
        # optional join table


    finally:
        conn.close()


if __name__ == "__main__":
    main()