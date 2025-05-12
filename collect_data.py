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

# Write the data to be stored for the generation of the script
with open('data/weather_data.json', 'w') as f:
    json.dump(weather_forecasts, f)


news_headlines = get_guardian_news_today_json()
print(news_headlines)

with open('data/news_headlines.json', 'w') as f:
    json.dump(news_headlines, f)


primary_emails = get_top_emails_json(max_results=5)

with open('data/primary_emails.json','w') as f:
    json.dump(primary_emails, f)

available_calendars = list_available_calendars()

full_calendars = {} # empty object to store results

for calendar_dict in available_calendars:
    # retrieve upcoming events for that calendar, for now we'll just set it to three days
    upcoming_events = get_upcoming_events_json(calendar_ids=[calendar_dict['id']], days=3)
    # store the upcoming events
    full_calendars[calendar_dict['summary']] = upcoming_events

with open('data/full_calendars.json', 'w') as f:
    json.dump(full_calendars, f)

# %%

# Example: Fetch events from all available calendars
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

# %%
# --- End Test Calendar Retrieval ---
