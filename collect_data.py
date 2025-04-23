import sys
import os
import json
from src.weather import get_forecast_by_city, get_forecast_by_zip_code

# collect weather data example
# print(get_forecast_by_city("London", 6))

# Example of how to work with the default.json

def load_config():
    """Load settings configuration from the default.json file"""
    config_path = os.path.join('config', 'default.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config() # config acts a dictionary of dictionaries for our stored settings

weather_forecasts =  get_forecast_by_zip_code(config['weather']['post_code'],config['weather']['country_code'],config['weather']['forecasts_to_give'])   
print(weather_forecasts)
