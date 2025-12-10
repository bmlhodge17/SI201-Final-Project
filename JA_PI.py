# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % mkdir -p ~/.kaggle
# mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
# chmod 600 ~/.kaggle/kaggle.json

# (base) jasmineabu@Jasmines-MacBook-Air-6 SI201-Final-Project % kaggle datasets list

#the api key is in downloads called kaggle.json
import pandas as pd

df = pd.read_csv('./kaggle data base/cities.csv')
print(df.head())

# Assuming the CSV file is in the specified path
# and the file name is 'cities.csv'
# The code reads the CSV file into a DataFrame and prints the first few rows
# to verify the data has been loaded correctly.



