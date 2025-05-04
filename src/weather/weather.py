import os
import requests
from datetime import datetime

# Load in .env variables from config (api keys)
from src.utils.config import API_KEY_OPEN_WEATHER

# add functions for returning raw json responses

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
    
    api_key = API_KEY_OPEN_WEATHER
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
    
    api_key = API_KEY_OPEN_WEATHER
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

def get_current_weather_city(city: str):
    """ Get current weather for a city. Returns a dictionary of time, temperature, wind speed, humidity, weather description, cloudiness percentage and sunset time. 
    Args:
        city (str): city for weather forecast
    """
    # Note future extension to add in error handling for incorrect city names or error status code from API
    units = 'metric'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_OPEN_WEATHER}&units={units}"
    response = requests.get(url)
    data = response.json()
    current_weather = {}
    current_weather['time'] = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S') # convert from unix
    current_weather['temp'] = data['main']['temp']
    current_weather['wind_speed'] = data['wind']['speed']
    current_weather['humidity'] = data['main']['humidity']
    current_weather['weather_desc'] = data['weather'][0]['description']
    current_weather['cloudiness'] = data['clouds']['all']
    current_weather['sunset_time'] = datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S') #convert from unix
    return current_weather

def get_current_weather_zipcode(zip_code: str, country_code: str):
    """ Get current weather for a zip code with country code. Returns a dictionary of time, temperature, wind speed, humidity, weather description, cloudiness percentage and sunset time. 
    Args:
        zip_code (str): location zipcode (first part of uk zip, eg. e1 or nw1)
        country_code (str): country code of zipcode
    """
    # Note future extension to add in error handling for incorrect city names or error status code from API
    units = 'metric'
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={API_KEY_OPEN_WEATHER}&units={units}"
    response = requests.get(url)
    data = response.json()
    current_weather = {}
    current_weather['time'] = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S') # convert from unix
    current_weather['temp'] = data['main']['temp']
    current_weather['wind_speed'] = data['wind']['speed']
    current_weather['humidity'] = data['main']['humidity']
    current_weather['weather_desc'] = data['weather'][0]['description']
    current_weather['cloudiness'] = data['clouds']['all']
    current_weather['sunset_time'] = datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S') #convert from unix
    return current_weather


if __name__ == "__main__":
    result = get_forecast_by_zip_code('wc1e', 'gb', 3)
    print(result)
