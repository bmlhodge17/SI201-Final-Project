import requests
import json

#take 100 cities from bris api so we share them
#and so i can make a json file of weather data for 100 cities
API_KEY = "b4e833d38c9ea664b0cd9c76f2c84a6f"

#bris api url
CITYBIKE_URL = "https://api.citybik.es/v2/networks"

#my weather api url
WEATHER_URL = "http://api.weatherstack.com/current"

# gets up to 100 unique city names from the citybike api
def get_100_cities():
    resp = requests.get(CITYBIKE_URL, timeout=20)
    data = resp.json().get("networks", [])

    cities = []
    seen = set()

    for net in data:
        city = net.get("location", {}).get("city")
        # skip empty or duplicate cities
        if city and city.lower() not in seen:
            cities.append(city)
            seen.add(city.lower())

        if len(cities) == 100:
            break

    return cities

# calls weatherstack api for one city
def get_weather(city_name):
    resp = requests.get(
        WEATHER_URL,
        params={
            "access_key": API_KEY,
            "query": city_name
        },
        timeout=15
    )

    data = resp.json()
 # weatherstack returns success=false when it fails
    if data.get("success") is False:
        return None
    
# return only the info we care about
#temp, uv index, description
    return {
        "city": city_name,
        "weather_description": data.get("current", {}).get("weather_descriptions"),
        "temperature_c": data.get("current", {}).get("temperature"),
        "uv_index": data.get("current", {}).get("uv_index")
    }


def main():
 # get 100 cities from bri’s api
    cities = get_100_cities()
    print(f"pulled {len(cities)} cities")

    results = []

    # loop through cities and call weather api
    for city in cities:
        weather = get_weather(city)
      # only save successful api calls
        if weather:
            results.append(weather)
            print("added:", city)
            
     # save everything to a json file
    with open("weather_100_cities.json", "w") as f:
        json.dump(results, f, indent=4)

    print("saved to weather_100_cities.json")


if __name__ == "__main__":
    main()