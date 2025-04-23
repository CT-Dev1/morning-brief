import os
from dotenv import load_dotenv

# This script is where we load our environment variables
# Script is used by modules like weather to import specific environment variables, so we don't have to call load_dotenv() constantly

# Load environment variables
load_dotenv()

API_KEY_OPEN_WEATHER = os.getenv("API_KEY_OPEN_WEATHER")

