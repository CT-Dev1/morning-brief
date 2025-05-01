import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for reading calendar events and list
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events.readonly"] # Added events scope for clarity
# Define paths relative to this script's location
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json") # Use a separate token file
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "oauth_credentials.json") # Use separate credentials if needed, or point to a shared one

def _get_calendar_service():
    """Handles authentication and returns the Calendar API service client."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Error loading calendar credentials from {TOKEN_PATH}: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing calendar token: {e}")
                # Fallback to re-authentication
                creds = None # Ensure creds is None so the next block runs
        # This block runs if creds is None initially, or if refresh failed
        if not creds:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"Error: Calendar credentials file not found at {CREDENTIALS_PATH}")
                return None
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error during calendar authentication flow: {e}")
                return None
        # Save the credentials for the next run (only if new or refreshed)
        try:
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
            print(f"Calendar credentials saved/updated in {TOKEN_PATH}")
        except Exception as e:
            print(f"Error saving calendar token to {TOKEN_PATH}: {e}")

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred building calendar service: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred building service: {e}")
        return None


def get_upcoming_events_json(calendar_ids=['primary'], days=5):
    """
    Fetches upcoming events from the specified Google Calendars for the next N days.

    Handles OAuth 2.0 authentication flow. Requires 'oauth_credentials.json'
    (or adjust path). Stores/uses 'token.json' for credentials.

    Args:
        calendar_ids (list): A list of calendar IDs to fetch events from.
                             Defaults to ['primary'].
        days (int): The number of days ahead to fetch events for. Defaults to 5.

    Returns:
        list: A list of dictionaries, where each dictionary represents an event
              with keys like 'summary', 'start', 'end', 'description', 'location', 'calendar_id'.
              Returns an empty list if an error occurs or no events are found.
    """
    service = _get_calendar_service()
    if not service:
        return []

    all_events_list = []
    try:
        # Get the start and end time for the query
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        time_min = now.isoformat()
        time_max = (now + datetime.timedelta(days=days)).isoformat()

        print(f"Getting upcoming events for the next {days} days from calendars: {', '.join(calendar_ids)}")

        for cal_id in calendar_ids:
            try:
                events_result = (
                    service.events()
                    .list(
                        calendarId=cal_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                if not events:
                    print(f"No upcoming events found in calendar '{cal_id}' for the specified timeframe.")
                    continue # Move to the next calendar ID

                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    end = event["end"].get("dateTime", event["end"].get("date"))
                    all_events_list.append({
                        'summary': event.get('summary', 'No Title'),
                        'start': start,
                        'end': end,
                        'description': event.get('description', ''),
                        'location': event.get('location', ''),
                        'calendar_id': cal_id # Add calendar ID to know the source
                    })
            except HttpError as error:
                 print(f"An error occurred fetching events for calendar '{cal_id}': {error}")
                 # Optionally parse error details as before
                 continue # Continue with other calendars if one fails

        # Sort all collected events by start time
        all_events_list.sort(key=lambda x: x['start'])

        return all_events_list

    except HttpError as error:
        # Catch errors related to the overall process if any (less likely now)
        print(f"An overall error occurred fetching calendar events: {error}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def list_available_calendars():
    """
    Lists all calendars the user has access to.

    Handles OAuth 2.0 authentication flow.

    Returns:
        list: A list of dictionaries, where each dictionary represents a calendar
              with keys 'id', 'summary', 'accessRole'. Returns an empty list on error.
    """
    service = _get_calendar_service()
    if not service:
        return []

    calendars_list = []
    try:
        print("Fetching list of available calendars...")
        page_token = None
        while True:
            calendar_list_result = service.calendarList().list(pageToken=page_token).execute()
            items = calendar_list_result.get('items', [])
            for calendar_list_entry in items:
                calendars_list.append({
                    'id': calendar_list_entry['id'],
                    'summary': calendar_list_entry.get('summary', 'No Summary'),
                    'accessRole': calendar_list_entry.get('accessRole', 'unknown')
                })
            page_token = calendar_list_result.get('nextPageToken')
            if not page_token:
                break
        print(f"Found {len(calendars_list)} calendars.")
        return calendars_list

    except HttpError as error:
        print(f"An error occurred fetching the calendar list: {error}")
        # Optionally parse error details
        return []
    except Exception as e:
        print(f"An unexpected error occurred listing calendars: {e}")
        return []


# Example usage (optional, for direct script testing)
if __name__ == "__main__":
    # List calendars first
    available_calendars = list_available_calendars()
    if available_calendars:
        print("\n--- Available Calendars ---")
        print(json.dumps(available_calendars, indent=2))

        # Example: Get events from the primary calendar only
        print("\n--- Events from Primary Calendar ---")
        primary_events = get_upcoming_events_json(calendar_ids=['primary'], days=7)
        if primary_events:
            print(json.dumps(primary_events, indent=2))
        else:
            print("Could not retrieve primary events.")

        # Example: Get events from the first two available calendars (if more than one exists)
        if len(available_calendars) > 1:
             cal_ids_to_fetch = [cal['id'] for cal in available_calendars[:2]]
             print(f"\n--- Events from Calendars: {', '.join(cal_ids_to_fetch)} ---")
             multi_cal_events = get_upcoming_events_json(calendar_ids=cal_ids_to_fetch, days=3)
             if multi_cal_events:
                 print(json.dumps(multi_cal_events, indent=2))
             else:
                 print("Could not retrieve events from multiple calendars.")

    else:
        print("Could not retrieve the list of available calendars.")
