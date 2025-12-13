import sqlite3 
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_Data_base = os.path.join(BASE_DIR, "JAB_Database.db")

def connect_to_database():
    print("Using database at:", SQL_Data_base)

    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    #cur.execute("DROP TABLE IF EXISTS cities;")  # run once if needed

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT NOT NULL,
        country TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        UNIQUE(city_name, city_id)
    );
    """)

    url = "https://api.citybik.es/v2/networks"
    networks = requests.get(url).json().get("networks", [])

    for n in networks:
        loc = n.get("location", {})
        city = loc.get("city")
        country = loc.get("country")

        if city is None or country is None:
            continue

        cur.execute("""
        INSERT OR IGNORE INTO cities (city_name, country, latitude, longitude)
        VALUES (?, ?, ?, ?)
        """, (
            city,
            country,
            loc.get("latitude"),
            loc.get("longitude")
        ))

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM cities")
    print("Rows in cities table:", cur.fetchone()[0])

    conn.close()


def main():
    connect_to_database()

if __name__ == "__main__":
    main()