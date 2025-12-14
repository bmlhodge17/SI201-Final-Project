import os
import re
import sqlite3
import requests
from datetime import datetime
import json

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
#loading the data:

# def cost_index_table(conn: sqlite3.Connection) -> None:
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS cost_index (
#             city_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             city TEXT UNIQUE NOT NULL,
#             cost_index REAL,
#             monthly_salary REAL
#         );
#     """)
#     conn.commit()


# def load_cost_cities_json(path: str) -> list[dict]:
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)


# def limit_cost(
#     conn: sqlite3.Connection,
#     cost_cities: list[dict],
#     limit: int = 25
# ) -> None:

#     insert_sql = """
#         INSERT OR IGNORE INTO cost_index
#         (city, cost_index, monthly_salary)
#         VALUES (?, ?, ?);
#     """

#     cur = conn.cursor()
#     added = 0

#     for item in cost_cities:
#         if added >= limit:
#             break

#         raw_city = item.get("City")
#         cost     = item.get("Cost_Index")
#         salary   = item.get("Average Monthly Net Salary (After Tax)")

#         if not raw_city:
#             continue

#         city_norm = canon_city(raw_city)

#         cur.execute(
#             insert_sql,
#             (city_norm, cost, salary)
#         )

#         if cur.rowcount == 1:
#             added += 1

#     conn.commit()
#     print(f"New rows inserted: {added}")



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
    try:
        cost_rows = load_cost_cities_json("cities_living_cost.json")

        cost_index_table(conn)
        limit_cost(conn, cost_rows, limit=25)

        total = conn.execute(
            "SELECT COUNT(*) FROM cost_index;"
        ).fetchone()[0]
        print("Total rows in cost_index:", total)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
 