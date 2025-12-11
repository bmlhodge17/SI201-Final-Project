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

JA_Data_base = "Jasmine.db"

def cost_index_table():
    conn = sqlite3.connect(JA_Data_base)
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

    

def plot_top_15_salaries(db_path="Jasmine.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Select city names and monthly salary
    cur.execute("""
        SELECT city_name, monthly_salary
        FROM cost_index
        WHERE monthly_salary IS NOT NULL
    """)
    rows = cur.fetchall()
    conn.close()

    # Sort by salary descending and take top 15
    top15 = sorted(rows, key=lambda x: x[1], reverse=True)[:15]

    # Separate lists for plotting
    cities = [city for city, salary in top15]
    salaries = [salary for city, salary in top15]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(cities, salaries, color='skyblue')
    plt.title("Top 15 Cities by Average Monthly Salary")
    plt.xlabel("City")
    plt.ylabel("Monthly Salary (USD)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Call the function
plot_top_15_salaries()



def main():
    
    plot_top_15_salaries()

if __name__ == "__main__":
    main()
