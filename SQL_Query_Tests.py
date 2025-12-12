import sqlite3 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_Data_base = os.path.join(BASE_DIR, "AB_SQL_Data_base.db")

def connect_to_database():
    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    return conn, cur


def select_stations():
    conn, cur = connect_to_database()
    query = ('''
             CREATE TABLE IF NOT EXISTS temp_sql_query_results
        SELECT *
            FROM stations
            WHERE city_id = '428'


    ''')


    conn.commit()
    conn.close()

def main():
    select_stations

if __name__ == "__main__":
    main()