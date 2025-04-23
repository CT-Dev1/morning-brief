import sys
import os
from src.weather import get_forecast_by_city, get_forecast_by_zip_code

# Add project root directory to Python's path - probably a more elegant way of doing this - enables modules to be found
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Down the line, add a setup.py at the root, restructure everything under src as importable code - see issue #1

from src.weather import get_forecast_by_city, get_forecast_by_zip_code

# collect weather data 
print(get_forecast_by_city("London", 6))

