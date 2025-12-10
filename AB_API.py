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
    11: "Austin",
    12: "Jacksonville",
    13: "Fort Worth",
    14: "Columbus",
    15: "Charlotte",
    16: "San Francisco",
    17: "Indianapolis",
    18: "Seattle",
    19: "Denver",
    20: "Washington",
    21: "Boston",
    22: "El Paso",
    23: "Nashville",
    24: "Detroit",
    25: "Oklahoma City",
    26: "Portland",
    27: "Las Vegas",
    28: "Memphis",
    29: "Louisville",
    30: "Baltimore",
    31: "Milwaukee",
    32: "Albuquerque",
    33: "Tucson",
    34: "Fresno",
    35: "Sacramento",
    36: "Mesa",
    37: "Kansas City",
    38: "Atlanta",
    39: "Omaha",
    40: "Colorado Springs",
    41: "Raleigh",
    42: "Miami",
    43: "Long Beach",
    44: "Virginia Beach",
    45: "Oakland",
    46: "Minneapolis",
    47: "Tulsa",
    48: "Arlington",
    49: "Tampa",
    50: "New Orleans",
    51: "Wichita",
    52: "Cleveland",
    53: "Bakersfield",
    54: "Aurora",
    55: "Anaheim",
    56: "Honolulu",
    57: "Corpus Christi",
    58: "Lexington",
    59: "Stockton",
    60: "Henderson",

    # International Cities
    61: "Toronto",
    62: "Vancouver",
    63: "Mexico City",
    64: "São Paulo",
    65: "Buenos Aires",
    66: "London",
    67: "Paris",
    68: "Berlin",
    69: "Madrid",
    70: "Rome",
    71: "Amsterdam",
    72: "Dublin",
    73: "Zurich",
    74: "Vienna",
    75: "Prague",
    76: "Warsaw",
    77: "Stockholm",
    78: "Oslo",
    79: "Copenhagen",
    80: "Reykjavik",
    81: "Tokyo",
    82: "Seoul",
    83: "Beijing",
    84: "Shanghai",
    85: "Hong Kong",
    86: "Singapore",
    87: "Bangkok",
    88: "Manila",
    89: "Jakarta",
    90: "New Delhi",
    91: "Mumbai",
    92: "Dubai",
    93: "Riyadh",
    94: "Istanbul",
    95: "Cairo",
    96: "Cape Town",
    97: "Nairobi",
    98: "Sydney",
    99: "Melbourne",
    100: "Auckland"
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








