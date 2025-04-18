# This script will periodically collect and store the weather data from a list of cities 

# %%

import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv


cities = ['London', 'Paris', 'Amsterdam', 'Copenhagen', 'Edinburgh', 'Barcelona', 'Rome', 'Berlin']

city = cities[0]

now = datetime.now()

load_dotenv()

def get_weather_data(city):
    '''Retrieves json response from open weather API for specific city. Returns dictionary object'''
    units = "metric"
    api_key = os.getenv("API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)

current_weather = pd.DataFrame({
        'city': [],
        'time': [],
        'weather':[]
    })

for city in cities:
    data = get_weather_data(city)
    new_row = pd.DataFrame({'city':[city], 'time': [now], 'weather':[data]})
    current_weather = pd.concat([current_weather, new_row], ignore_index=True)
 
# %%    

# Save the current weather data to a pickle file
if os.path.exists('weather_history.pkl'):
    print("found existing weather_history.pkl")
    past_weather = pd.read_pickle('weather_history.pkl')
    updated_weather = pd.concat([past_weather, current_weather], ignore_index=True)
else:
    print("no existing weather history found, creating new pkl file")
    updated_weather = current_weather

updated_weather.to_pickle('weather_history.pkl')

# %%

# Now we'll practice loading the file to get yesterday's weather

weather_history = pd.read_pickle('weather_history.pkl')

weather_history.info()

# Sort the data frame by time so the latest recordings at the bottom of the df
weather_history.sort_values(by='time', ascending=True, inplace = True) # add the inplace = True to specify 

weather_history

# Get recorded weather data from yesterday

current_city = "London"

# the below is definitely bad code because it will break 
yesterday_data = weather_history[(weather_history['city'] == current_city) & (weather_history['time'].date == now.date()-1)]


# %%

# Run analytics on the recent weather history




# %%

# Realistically you can improve all of the above by using
# the historical weather api that can use your exact location etc.

