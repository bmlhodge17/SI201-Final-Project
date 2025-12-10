# import json
# import os
# import unittest
# import sqlite3
# import requests


# API_Key = "9dd604ce-a65f-43e1-9d27-7f87d214a75c"
 
# def get_countries_url(): 
#     url = f"http://api.airvisual.com/v2/countries?key={API_Key}"
#     response = requests.get(url)
#     response_json = response.json()
#     return (response_json, url) if response_json.get("status") == 'success' else print('None')  

# def get_supported_states(country_name): #has one paramenter
#     url = f"http://api.airvisual.com/v2/states?country={country_name}&key={API_Key}"
#     response = requests.get(url)
#     response_json = response.json()
#     return (response_json, url) if response_json.get("status") == 'success' else print('None')  

# def get_supported_cities(country_name, state_name): #has two paramenters
#     url = f"http://api.airvisual.com/v2/cities?state={state_name}&country={country_name}&key={API_Key}"
#     response = requests.get(url)
#     response_json = response.json()
#     return (response_json, url) if response_json.get("status") == 'success' else print('None')

# # def get_city_data(country_name, state_name, city_name): #has 3 paramenters
# #     url = f"http://api.airvisual.com/v2/city?city={city_name}&state={state_name}&country={country_name}&key={API_Key}"
# #            #http://api.airvisual.com/v2/city?city={{CITY_NAME}}&state={{STATE_NAME}}&country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}
# #     response = requests.get(url)
# #     response_json = response.json()
# #     return (response_json, url) if response_json.get("status") == 'success' else print('None')



# # ---- 1. City list ----

# cities = [
#     "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
#     "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
#     "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
#     "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
#     "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
#     "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
#     "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
#     "Mesa", "Kansas City", "Atlanta", "Omaha", "Colorado Springs",
#     "Raleigh", "Miami", "Long Beach", "Virginia Beach", "Oakland",
#     "Minneapolis", "Tulsa", "Arlington", "Tampa", "New Orleans",
#     "Wichita", "Cleveland", "Bakersfield", "Aurora", "Anaheim",
#     "Honolulu", "Corpus Christi", "Lexington", "Stockton", "Henderson",

#     "Toronto", "Vancouver", "Mexico City", "São Paulo", "Buenos Aires",
#     "London", "Paris", "Berlin", "Madrid", "Rome", "Amsterdam",
#     "Dublin", "Zurich", "Vienna", "Prague", "Warsaw", "Stockholm",
#     "Oslo", "Copenhagen", "Reykjavik",

#     "Tokyo", "Seoul", "Beijing", "Shanghai", "Hong Kong", "Singapore",
#     "Bangkok", "Manila", "Jakarta", "New Delhi",

#     "Mumbai", "Dubai", "Riyadh", "Istanbul", "Cairo", "Cape Town",
#     "Nairobi", "Sydney", "Melbourne", "Auckland"
# ]

# # ---- 2. State lookup for U.S. cities ----

# us_states = {
#     "New York": "New York",
#     "Los Angeles": "California",
#     "Chicago": "Illinois",
#     "Houston": "Texas",
#     "Phoenix": "Arizona",
#     "Philadelphia": "Pennsylvania",
#     "San Antonio": "Texas",
#     "San Diego": "California",
#     "Dallas": "Texas",
#     "San Jose": "California",
#     "Austin": "Texas",
#     "Jacksonville": "Florida",
#     "Fort Worth": "Texas",
#     "Columbus": "Ohio",
#     "Charlotte": "North Carolina",
#     "San Francisco": "California",
#     "Indianapolis": "Indiana",
#     "Seattle": "Washington",
#     "Denver": "Colorado",
#     "Washington": "District of Columbia",
#     "Boston": "Massachusetts",
#     "El Paso": "Texas",
#     "Nashville": "Tennessee",
#     "Detroit": "Michigan",
#     "Oklahoma City": "Oklahoma",
#     "Portland": "Oregon",
#     "Las Vegas": "Nevada",
#     "Memphis": "Tennessee",
#     "Louisville": "Kentucky",
#     "Baltimore": "Maryland",
#     "Milwaukee": "Wisconsin",
#     "Albuquerque": "New Mexico",
#     "Tucson": "Arizona",
#     "Fresno": "California",
#     "Sacramento": "California",
#     "Mesa": "Arizona",
#     "Kansas City": "Missouri",
#     "Atlanta": "Georgia",
#     "Omaha": "Nebraska",
#     "Colorado Springs": "Colorado",
#     "Raleigh": "North Carolina",
#     "Miami": "Florida",
#     "Long Beach": "California",
#     "Virginia Beach": "Virginia",
#     "Oakland": "California",
#     "Minneapolis": "Minnesota",
#     "Tulsa": "Oklahoma",
#     "Arlington": "Texas",
#     "Tampa": "Florida",
#     "New Orleans": "Louisiana",
#     "Wichita": "Kansas",
#     "Cleveland": "Ohio",
#     "Bakersfield": "California",
#     "Aurora": "Colorado",
#     "Anaheim": "California",
#     "Honolulu": "Hawaii",
#     "Corpus Christi": "Texas",
#     "Lexington": "Kentucky",
#     "Stockton": "California",
#     "Henderson": "Nevada"
# }

# # ---- 3. Country lookup for international cities ----

# international_countries = {
#     "Toronto": ("Canada", "Ontario"),
#     "Vancouver": ("Canada", "British Columbia"),
#     "Mexico City": ("Mexico", "Mexico City"),
#     "São Paulo": ("Brazil", "Sao Paulo"),
#     "Buenos Aires": ("Argentina", "Buenos Aires"),
#     "London": ("United Kingdom", "England"),
#     "Paris": ("France", "Ile-de-France"),
#     "Berlin": ("Germany", "Berlin"),
#     "Madrid": ("Spain", "Madrid"),
#     "Rome": ("Italy", "Lazio"),
#     "Amsterdam": ("Netherlands", "North Holland"),
#     "Dublin": ("Ireland", "Leinster"),
#     "Zurich": ("Switzerland", "Zurich"),
#     "Vienna": ("Austria", "Vienna"),
#     "Prague": ("Czechia", "Prague"),
#     "Warsaw": ("Poland", "Mazovia"),
#     "Stockholm": ("Sweden", "Stockholm"),
#     "Oslo": ("Norway", "Oslo"),
#     "Copenhagen": ("Denmark", "Capital Region"),
#     "Reykjavik": ("Iceland", "Capital Region"),
#     "Tokyo": ("Japan", "Tokyo"),
#     "Seoul": ("South Korea", "Seoul"),
#     "Beijing": ("China", "Beijing"),
#     "Shanghai": ("China", "Shanghai"),
#     "Hong Kong": ("Hong Kong", "Hong Kong"),
#     "Singapore": ("Singapore", "Singapore"),
#     "Bangkok": ("Thailand", "Bangkok"),
#     "Manila": ("Philippines", "Metro Manila"),
#     "Jakarta": ("Indonesia", "Jakarta"),
#     "New Delhi": ("India", "Delhi"),
#     "Mumbai": ("India", "Maharashtra"),
#     "Dubai": ("UAE", "Dubai"),
#     "Riyadh": ("Saudi Arabia", "Riyadh"),
#     "Istanbul": ("Turkey", "Istanbul"),
#     "Cairo": ("Egypt", "Cairo"),
#     "Cape Town": ("South Africa", "Western Cape"),
#     "Nairobi": ("Kenya", "Nairobi"),
#     "Sydney": ("Australia", "New South Wales"),
#     "Melbourne": ("Australia", "Victoria"),
#     "Auckland": ("New Zealand", "Auckland")
# }

# # ---- 4. Function to call your API ----

# def get_city_data(country, state, city):
#     url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={API_Key}"
#     response = requests.get(url)
    
#     try:
#         data = response.json()
#     except:
#         return None

#     if data.get("status") == "success":
#         return data
#     return None

# # ---- 5. Build the JSON list ----

# final_output = []

# for city in cities:

#     if city in us_states:
#         country = "USA"
#         state = us_states[city]
#     else:
#         country, state = international_countries[city]

#     #print(f"Fetching: {city}, {state}, {country}")

#     data = get_city_data(country, state, city)
#     #time.sleep(1)   # prevent API rate limit

#     final_output.append({
#         "city": city,
#         "state": state,
#         "country": country,
#         "air_quality": data if data else "No Data Returned"
#     })

# # ---- 6. Save JSON ----

# with open("all_city_air_quality.json", "w") as f:
#     json.dump(final_output, f, indent=4)

# print("Saved to all_city_air_quality.json")





# # def main():
# #     data = get_city_data('India', 'Delhi', 'New Delhi')
# #     if data:
# #         # Save it to a file
# #         with open("get_city_data.json", "w") as f:
# #             json.dump(data, f, indent=4)   
# #         print("Saved to get_city_data.json")

# # #calls everything
# # main()



# #main()

pip install kaggle

