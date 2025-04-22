# Set up block
# %%
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv() # assume .env file in file folder

cities = ['London', 'Paris', 'Amsterdam', 'Copenhagen', 'Edinburgh', 'Barcelona', 'Rome', 'Berlin']

city = cities[0]

# %%

# Weather forecast API endpoint
# https://openweathermap.org/forecast5 for documentation
# Endpoint: api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
# Goal: Get weather forecast for the day in three hour intervals, output comprehendable string object

units = "metric"
api_key = os.getenv("API_KEY")
cnt = 3 # the number of timestamps which will be returned in the API response
zip_code = "e1"
country_code = "gb"

url = f"http://api.openweathermap.org/data/2.5/forecast?zip=e1,gb&appid={api_key}&units={units}"
response = requests.get(url)

# test response
if response.status_code == 200:
    data = response.json()
    print(data.items())
else:
    print("error")
    print(response.status_code)
    
print(json.dumps(data, indent = 5))
# %%
print(json.dumps(data, indent= 4))

# Get forecast for the next three hours 
print(data['list'][0])

forecast_next_3_hours = data['list'][0]
# forecast time 
print(datetime.strftime(datetime.fromtimestamp(forecast_next_3_hours['dt']), '%Y-%m-%d %H:%M:%S'))

# %%

# function for the weather forecast by city
def get_forecast_by_city(city: str, num_forecast : int):
    """ Get weather forecasts for a city, returns a list of dictionaries.
    Forecasts include time, temperature, wind_speed, humidity, weather_description, 
    cloudiness percentage, probability of precipitation.
    Args:
        city (str): city for weather forecast
        num_forecast (int): number of forecasts (in 3 hour intervals) to return
        
    """    
    # Note: future extension, possibility to change num_forecast to hours to forecast to add better control
    # Add error handling for:
    # improperly formatted city names, or negative forecast number inputs
    # API errors
    
    api_key = os.getenv("API_KEY")
    units = "metric"
    cnt = num_forecast
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}&cnt={cnt}"
    response = requests.get(url)
    data = response.json()    
    forecasted_weather =[]
    for i in range(num_forecast):
        ith_forecast = {}
        weather = data['list'][i]
        ith_forecast['time'] = weather['dt_txt']
        ith_forecast['temp'] = weather['main']['temp']
        ith_forecast['wind_speed'] = weather['wind']['speed']
        ith_forecast['humidity'] = weather['main']['humidity']
        ith_forecast['weather_desc'] = weather['weather'][0]['description']
        ith_forecast['cloudiness'] = weather['clouds']['all']
        ith_forecast['precipitation_prob'] = weather['pop']
        forecasted_weather.append(ith_forecast)
    return forecasted_weather

# %%
# function for weather forecast by zip code and country code
def get_forecast_by_zip_code(zip_code :str, country_code: str, num_forecast: int):
    """ Get weather forecasts for a zip code, returns a list of dictionaries.
    Forecasts include time, temperature, wind_speed, humidity, weather_description, 
    cloudiness percentage, probability of precipitation.
    Args:
        zip_code (str): location zipcode (first part of uk zip, eg. e1 or nw1)
        country_code (str): country code of zipcode
        num_forecast (int): number of forecasts (in 3 hour intervals) to return
        
    """    
    # Note: future extension, possibility to change num_forecast to hours to forecast to add better control
    # Add error handling for:
    # improperly formatted zip code inputs or country codes, 
    # or negative forecast number inputs
    # API errors
    
    api_key = os.getenv("API_KEY")
    units = "metric"
    cnt = num_forecast 
    url = f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={api_key}&units={units}&cnt={cnt}"
    response = requests.get(url)
    data = response.json()    
    forecasted_weather =[]
    for i in range(num_forecast):
        ith_forecast = {}
        weather = data['list'][i]
        ith_forecast['time'] = weather['dt_txt']
        ith_forecast['temp'] = weather['main']['temp']
        ith_forecast['wind_speed'] = weather['wind']['speed']
        ith_forecast['humidity'] = weather['main']['humidity']
        ith_forecast['weather_desc'] = weather['weather'][0]['description']
        ith_forecast['cloudiness'] = weather['clouds']['all']
        ith_forecast['precipitation_prob'] = weather['pop']
        forecasted_weather.append(ith_forecast)
    return forecasted_weather

# %%

# Weather history API endpoint
# https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API key}
# See https://openweathermap.org/history for documentation

# Aim - get the previous 

# get lat, long for your house from the geocoder api below
# get start, end time in unix time

