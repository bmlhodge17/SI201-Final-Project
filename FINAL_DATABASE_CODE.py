import os
import re
import sqlite3
import requests
from datetime import datetime

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



def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        networks = fetch_networks()
        upsert_cities(conn, networks)

        # optional: show total rows in the table
        total = conn.execute("SELECT COUNT(*) FROM cities;").fetchone()[0]
        print(f"Total rows in `cities`: {total}")
    finally:
        conn.close()


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

# weather table functions
API_KEY = "b4e833d38c9ea664b0cd9c76f2c84a6f"

# weather table initialization
def init_weather_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            city_name TEXT NOT NULL,
            weather_city TEXT,
            weather_description TEXT,
            updated_at TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(city_id)
        );
        """
    )
     # check if city_name column exists
     #this prevents errors if the table already exists
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(weather);")
    columns = [col[1] for col in cur.fetchall()]

    # add city_name only if missing
    if "city_name" not in columns:
        cur.execute("ALTER TABLE weather ADD COLUMN city_name TEXT;")

    conn.commit()

# fetch weather data from API
def get_city_weather(city_name):
     # build request url using api key and city name
    url = (
        f"http://api.weatherstack.com/current"
        f"?access_key={API_KEY}&query={city_name}"
    )

    resp = requests.get(url, timeout=15)
    data = resp.json()
     # handle api errors
    if data.get("success") is False:
        print("WEATHERSTACK ERROR FOR", city_name, data)
        return None
        
    # sometimes api returns success but no current weather data
    current = data.get("current")
    if not current:
        print("NO CURRENT WEATHER FOR", city_name, data)
        return None
    
     # extract first weather description if available
    description = None
    if current.get("weather_descriptions"):
        description = current["weather_descriptions"][0]

    return {
        "weather_city": data.get("location", {}).get("name"),
        "weather_description": description
    }
# populate weather table
def populate_weather(conn, limit=25):
    cur = conn.cursor()

    # get city_id + city_name from bri’s table
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

    for city_id, city_name in cities:
    # call weather api (title() helps with api recognition)
        weather = get_city_weather(city_name.title())

     # skip insert if api failed
        if not weather:
            print("SKIPPING WEATHER INSERT FOR", city_name)
            continue

        print("INSERTING WEATHER FOR", city_name)

      # insert weather data into table
        cur.execute(
            """
            INSERT INTO weather
            (city_id, city_name, weather_city, weather_description, updated_at)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                city_id,
                city_name,
                weather.get("weather_city"),
                weather.get("weather_description"),
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )

        print("INSERTING:", city_id, city_name)

    conn.commit()
    print("weather table populated")


def main():
    # print database path to confirm correct db file
    print("USING DB FILE:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    # cities first (for the joins later)
    init_db(conn)
    networks = fetch_networks()
    upsert_cities(conn, networks)

    
    # confirm cities exist before adding weather
    count = conn.execute("SELECT COUNT(*) FROM cities;").fetchone()[0]
    print("CITIES COUNT BEFORE WEATHER:", count)

    #create weather table and populate it
    init_weather_table(conn)
    populate_weather(conn)

    conn.close()

#call main function
if __name__ == "__main__":
    main()
 