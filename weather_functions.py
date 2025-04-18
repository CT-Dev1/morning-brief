import requests

def get_weather_data(city):
    '''Retrieves json response from open weather API for specific city. Returns dictionary object'''
    units = "metric"
    api_key = "ff4b88bc79dcd581bf3afa2fef167363"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)


