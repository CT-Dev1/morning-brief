
# %%
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Weather forecast API endpoint
# https://openweathermap.org/forecast5 for documentation
# Endpoint: api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
# Goal: Get weather forecast for the day in three hour intervals, output comprehendable string object

# Load environment variables from .env file
load_dotenv() # assume .env file in file folder


cities = ['London', 'Paris', 'Amsterdam', 'Copenhagen', 'Edinburgh', 'Barcelona', 'Rome', 'Berlin']

city = cities[0]

units = "metric"
api_key = os.getenv("API_KEY")
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
response = requests.get(url)

# test response
if response.status_code == 200:
    data = response.json()
    print(data.items())


# function for the above







# %%

# Weather history API endpoint
# https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&cnt={cnt}&appid={API key}
# See https://openweathermap.org/history for documentation




# Add-on: Geocoder API to add in converstion between lat long coords and 
# geographic place names 
# url = http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}