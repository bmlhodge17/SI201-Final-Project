import unittest
import sqlite3
import os

'''
creating tables
what tables do we want to create? 

- city_id
- weather?
- date?

'''
SQL_Data_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SQL_Data_base.db")
#.py file creates our .db file

def connect_to_database():
    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    return conn, cur

#Create citybike tables
def create_citybike_tables():
    conn, cur = connect_to_database()

#cities table
    cur.execute('''
            CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE,
            country TEXT,
            latitude REAL,
            longitude REAL
        );

    ''')


#networks table (Citybikes/biking networks)
    cur.execute('''
            CREATE TABLE IF NOT EXISTS networks (
            network_id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_network_id TEXT UNIQUE,
            network_name TEXT,
            city_id INTEGER,
            FOREIGN KEY(city_id) REFERENCES cities(city_id)
        );
    ''')

#stations table
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
    conn.close()


def main():
    create_citybike_tables()

if __name__ == "__main__":
    main()