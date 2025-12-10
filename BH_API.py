# Name: Brianna Hodge
# Student ID: 50873856
# Email: bmlhodge@umich.edu
# Project Team Name: JAB
#Team Members: Brianna Hodge, Jasmine Abu, Asiah Bays
# List any AI tool (e.g. ChatGPT, GitHub Copilot): Sql cheatsheet, Chatgpt, Matplotlib Lecture Slides


#Notes for project: if you have dup string data maybe create a new table
#table columns: city, city_id, bikes, etc
#api is good to have 100 rows


import json
import os
import unittest
import sqlite3
import requests
import matplotlib.pyplot as plt

#get api url city bikes
api_url = "https://api.citybik.es/v2/networks"
response = requests.get(api_url)
data = response.json()
#print(data)


def fetch_networks_from_api():
    #Fetch all CityBikes networks from API and return json data
    api_url = "https://api.citybik.es/v2/networks"
    response = requests.get(api_url)
    data = response.json()
    return data["networks"]

#create our database (SQL_Data_base) and start creating tables




def main():
    pass

if __name__ == "__main__":
    main()

