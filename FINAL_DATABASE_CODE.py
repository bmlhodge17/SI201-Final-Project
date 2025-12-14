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
data = []
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Write JSON
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
    conn = sqlite3.connect(DB_PATH)
    
    #jasmines call
    try:
        cost_index_table(conn)        # CREATE TABLE ONLY
        upsert_cost_index(conn)       # inserts ≤25 rows

        total = conn.execute(
            "SELECT COUNT(*) FROM cost_index;"
        ).fetchone()[0]
        print(f"Total rows in `cost_index`: {total}")
    finally:
        conn.close()
    
if __name__ == "__main__":
    main()
 