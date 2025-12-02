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

def main():
    data = get_supported_states("India")
    if data:
        # Save it to a file
        with open("supported_states.json", "w") as f:
            json.dump(data, f, indent=4)   # pretty formatting
        print("Saved to supported_states.json")


main()