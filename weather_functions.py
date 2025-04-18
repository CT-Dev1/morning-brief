import requests
from dotenv import load_dotenv
import os


def get_weather_data(city):
    '''Retrieves json response from open weather API for specific city. Returns dictionary object'''
    load_dotenv()
    units = "metric"
    api_key = os.getenv("API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)


