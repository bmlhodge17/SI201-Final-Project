# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % mkdir -p ~/.kaggle
# mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
# chmod 600 ~/.kaggle/kaggle.json

# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % kaggle datasets list

#the api key is in downloads called kaggle.json
import pandas as pd
import csv
import json

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

#creating tables 
#1 table for cities and their id 


