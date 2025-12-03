import json
import os
import unittest
import sqlite3
import requests



API_Key = "9dd604ce-a65f-43e1-9d27-7f87d214a75c"
 
def get_countries_url():
    url = f"http://api.airvisual.com/v2/countries?key={API_Key}"
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')  

def get_supported_states(country_name):
    url = f"http://api.airvisual.com/v2/states?country={country_name}&key={API_Key}"
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')  

def get_supported_cities(country_name, state_name):
    url = f"http://api.airvisual.com/v2/cities?state={state_name}&country={country_name}&key={API_Key}"
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')

def get_city_data(country_name, state_name, city_name):
    url = f"http://api.airvisual.com/v2/city?city={city_name}&state={state_name}&country={country_name}&key={API_Key}"
           #http://api.airvisual.com/v2/city?city={{CITY_NAME}}&state={{STATE_NAME}}&country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')

def main():
    data = get_supported_cities('Ukraine', 'Cherkasy', "Umon")
    if data:
        # Save it to a file
        with open("city_data.json", "w") as f:
            json.dump(data, f, indent=4)   # pretty formatting
        print("Saved to city_data.json")


main()