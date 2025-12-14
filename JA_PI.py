# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % mkdir -p ~/.kaggle
# mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
# chmod 600 ~/.kaggle/kaggle.json

# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % kaggle datasets list

#the api key is in downloads called kaggle.json
import pandas as pd
import csv
import json
import sqlite3
import matplotlib.pyplot as plt
import os


df = pd.read_csv('./kaggle data base/cities.csv')
print(df.head())

# Assuming the CSV file is in the specified path
# and the file name is 'cities.csv'
# The code reads the CSV file into a DataFrame and prints the first few rows
# to verify the data has been loaded correctly.

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


import sqlite3
import json

import sqlite3
import json

SQL_Data_base = "JAB_Database.db"

def cost_index_table():
    conn = sqlite3.connect(SQL_Data_base)
    cur = conn.cursor()

    # 1. Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cost_index (
            city_name TEXT UNIQUE,
            monthly_salary REAL
        );
    """)

    conn.commit()

    # 2. Load JSON correctly
    with open("cities_living_cost.json", "r") as f:
        data = json.load(f)

    # 3. Insert rows
    for row in data:

        # Convert ID — JSON key name is literally ""
        #city_id = int(row.get("", 0))

        city_name = row.get("City", "Unknown")

        # Convert strings → floats safely
        #cost_index = float(row.get("Cost_index", 0) or 0)
        monthly_salary = float(row.get("Average Monthly Net Salary (After Tax)", 0) or 0)

        cur.execute("""
            INSERT OR REPLACE INTO cost_index (city_name, monthly_salary)
            VALUES (?, ?)
        """, (city_name, monthly_salary))

    conn.commit()
    conn.close()

    print("Cost index and salary data successfully loaded!")


    #calculation 
# def get_top_15_salaries(db_path="AB_SQL_Data_base.db"):


#     conn = sqlite3.connect(db_path)
#     cur = conn.cursor()

#     # Get city + salary, ignore NULLs
#     cur.execute("""
#         SELECT city_name, monthly_salary
#         FROM cost_index
#         WHERE monthly_salary IS NOT NULL
#     """)

#     rows = cur.fetchall()
#     conn.close()

#     # Convert salary strings -> float
#     cleaned = []
#     for city, salary in rows:
#         try:
#             salary_float = float(salary)
#             cleaned.append((city, salary_float))
#         except:
#             continue  # skip corrupted values

#     # Sort by salary descending and take top 15
#     top15 = sorted(cleaned, key=lambda x: x[1], reverse=True)[:15]
#     cities = [item[0] for item in top15]
#     salaries = [item[1] for item in top15]

#     #plot
#     plt.figure(figsize=(14, 7))
#     plt.bar(cities, salaries)
#     plt.title("Top 15 Cities by Monthly Salary index")
#     plt.xlabel("City")
#     plt.ylabel("Average Monthly Salary (USD)")
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()
#     plt.show()


    # print(cities)
    # print(salaries)

import matplotlib.pyplot as plt

# def plot_top_15_salaries(data):
#     """
#     Expects data in the format:
#     [('City1', salary1), ('City2', salary2), ...]
#     """

#     #sorting the data in decending order
#     #data.sort(key=lambda x: x[1], reverse=True)
#     # Separate cities and salaries
    
#     cities = (for city in data[0])
#     salaries = (for salary in (data[1]))
    

#     # Create the bar graph
#     plt.figure(figsize=(14, 7))
#     plt.bar(cities, salaries)
#     plt.title("Top 15 Cities by Monthly Salary")
#     plt.xlabel("City")
#     plt.ylabel("Average Monthly Salary (USD)")
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()
#     plt.show()




def main():
    
    cost_index_table()

if __name__ == "__main__":
    main()
