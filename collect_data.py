import sys
import os
import json
from src.weather import get_forecast_by_city, get_forecast_by_zip_code
from src.stocks import get_daily_time_series
from src.news import get_guardian_news_today_json
# Import the email function
from src.email_retrieve import get_top_emails_json

# collect weather data example
# print(get_forecast_by_city("London", 6))

# Example of how to work with the default.json

def load_config():
    """Load settings configuration from the default.json file"""
    config_path = os.path.join('config', 'default.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config() # config acts a dictionary of dictionaries for our stored settings

# Example of how to get weather data from src
weather_forecasts =  get_forecast_by_zip_code(config['weather']['post_code'],config['weather']['country_code'],config['weather']['forecasts_to_give'])   
print(weather_forecasts)


# Example of how to get stock price data from src
stock_price = get_daily_time_series("NVDA")

print(stock_price)

# Example of how to get recent news headline from guardian

news_headlines = get_guardian_news_today_json()
print(news_headlines)

# --- Test Email Retrieval ---
print("\n--- Fetching Primary Emails ---")
# You might want to request fewer emails for testing to speed things up
primary_emails = get_top_emails_json(max_results=5)

if primary_emails:
    print(f"Successfully retrieved {len(primary_emails)} primary emails.")
    # Optionally print details of the first email
    if primary_emails:
        print("\nDetails of the first email:")
        print(json.dumps(primary_emails[0], indent=2))
else:
    print("Could not retrieve primary emails or none found.")
# --- End Test Email Retrieval ---
