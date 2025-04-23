# Import functions from weather.py
from .weather import get_forecast_by_city, get_forecast_by_zip_code

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Make these functions available on import
__all__ = ['get_forecast_by_city', 'get_forecast_by_zip_code']