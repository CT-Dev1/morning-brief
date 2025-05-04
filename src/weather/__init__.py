# Import functions from weather.py
from .weather import get_forecast_by_city, get_forecast_by_zip_code, get_current_weather_zipcode, get_current_weather_city

# Make these functions available on import
__all__ = ['get_forecast_by_city', 'get_forecast_by_zip_code', 'get_current_weather_zipcode']