import os
from dotenv import load_dotenv
#import pathlib

# This script is where we load our environment variables
# Script is used by modules like weather to import specific environment variables, so we don't have to call load_dotenv() constantly

#dotenv_path = pathlib.Path(__file__).parent.parent.parent / '.env'

# Load environment variables
#load_dotenv(dotenv_path)
load_dotenv()

API_KEY_OPEN_WEATHER = os.getenv("API_KEY_OPEN_WEATHER")
GOOGLE_APP_CREDENTIALS_PATH = os.getenv("GOOGLE_APP_CREDENTIALS_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = os.getenv("SSH_PORT")    
SSH_USERNAME = os.getenv("SSH_USERNAME")
SSH_PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY")


