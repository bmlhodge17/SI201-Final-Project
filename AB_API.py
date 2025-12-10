import json
import os
import unittest
import sqlite3
import requests
from datetime import datetime, timedelta

API_key = "b4e833d38c9ea664b0cd9c76f2c84a6f"

import json
import requests

API_key = "b4e833d38c9ea664b0cd9c76f2c84a6f"


def get_city_weather(city_name):
    url = f"http://api.weatherstack.com/current?access_key={API_key}&query={city_name}"

    response = requests.get(url)

    try:
        response_json = response.json()
    except:
        return None

    # Weatherstack error handling
    if response_json.get("success") is False:
        return None

    return response_json, url


def main():

    # 100 cities (fill these out)
    cities = {
        1: "New York",
        2: "Los Angeles",
        3: "Chicago",
        4: "Houston",
        5: "Phoenix",
        6: "Philadelphia",
        7: "San Antonio",
        8: "San Diego",
        9: "Dallas",
        10: "San Jose",
        # continue to 100...
    }

    final_json = {
        "cities": []
    }

    for city_id, city_name in cities.items():
        data = get_city_weather(city_name)

        if not data:
            continue

        weather_json, url_used = data

        final_json["cities"].append({
            "city_id": city_id,
            "city_name": city_name,
            "request": weather_json.get("request", {}),
            "location": weather_json.get("location", {}),
            "current": weather_json.get("current", {}),
            "weatherstack_url": url_used
        })

    # Save file
    with open("weather_100_cities.json", "w") as f:
        json.dump(final_json, f, indent=4)

    print("Saved to weather_100_cities.json")


main()








