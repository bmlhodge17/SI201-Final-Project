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

def get_supported_states(country_name): #has one paramenter
    url = f"http://api.airvisual.com/v2/states?country={country_name}&key={API_Key}"
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')  

def get_supported_cities(country_name, state_name): #has two paramenters
    url = f"http://api.airvisual.com/v2/cities?state={state_name}&country={country_name}&key={API_Key}"
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')

def get_city_data(country_name, state_name, city_name): #has 3 paramenters
    url = f"http://api.airvisual.com/v2/city?city={city_name}&state={state_name}&country={country_name}&key={API_Key}"
           #http://api.airvisual.com/v2/city?city={{CITY_NAME}}&state={{STATE_NAME}}&country={{COUNTRY_NAME}}&key={{YOUR_API_KEY}}
    response = requests.get(url)
    response_json = response.json()
    return (response_json, url) if response_json.get("status") == 'success' else print('None')

# def get_global_city_ranking(country_name):
#     url = f"http://api.airvisual.com/v2/city_ranking?key={API_Key}&sort=&country={country_name}"
#     response = requests.get(url)
#     response_json = response.json()
#     return (response_json, url) if response_json.get("status") == 'success' else print('None')


def main():
    data = get_global_city_ranking(USA)
    if data:
        # Save it to a file
        with open("get_global_city_ranking.json", "w") as f:
            json.dump(data, f, indent=4)   
        print("Saved to get_global_city_ranking.json")

#calls everything
main()
