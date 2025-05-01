import sys
import os
import json
from src.weather import get_forecast_by_city, get_forecast_by_zip_code
from src.stocks import get_daily_time_series
from src.news import get_guardian_news_today_json
# Import the email function
from src.email_retrieve import get_top_emails_json
# Import the calendar functions
from src.calendar_retrieve import get_upcoming_events_json, list_available_calendars

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


# --- Test Calendar Retrieval ---
print("\n--- Listing Available Calendars ---")
available_calendars = list_available_calendars()

if available_calendars:
    print(f"Found {len(available_calendars)} calendars.")
    # Print summary of available calendars
    for i, cal in enumerate(available_calendars):
        print(f"  {i+1}. ID: {cal['id']}, Summary: {cal['summary']}, Role: {cal['accessRole']}")

    # Example: Fetch events only from the 'primary' calendar
    print("\n--- Fetching Upcoming Calendar Events (Primary, Next 5 Days) ---")
    primary_calendar_events = get_upcoming_events_json(calendar_ids=['primary'], days=5)

    if primary_calendar_events:
        print(f"Successfully retrieved {len(primary_calendar_events)} upcoming events from primary calendar.")
        if primary_calendar_events:
            print("\nDetails of the first upcoming event (Primary):")
            print(json.dumps(primary_calendar_events[0], indent=2))
    else:
        print("Could not retrieve upcoming events from primary calendar or none found.")

    # Example: Fetch events from all available calendars (use with caution if many calendars)
    # all_calendar_ids = [cal['id'] for cal in available_calendars]
    # print(f"\n--- Fetching Upcoming Calendar Events (All Calendars: {len(all_calendar_ids)}, Next 2 Days) ---")
    # all_events = get_upcoming_events_json(calendar_ids=all_calendar_ids, days=2)
    # if all_events:
    #     print(f"Successfully retrieved {len(all_events)} events from all calendars.")
    #     if all_events:
    #         print("\nDetails of the first upcoming event (All Calendars):")
    #         print(json.dumps(all_events[0], indent=2))
    # else:
    #      print("Could not retrieve events from all calendars.")

else:
    print("Could not retrieve the list of available calendars.")
# --- End Test Calendar Retrieval ---
