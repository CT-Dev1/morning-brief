import json
import requests
import datetime
from src.utils.config import GUARDIAN_API_KEY, NEWSDATA_API_KEY
from datetime import datetime, timedelta

# Guardian news today call function
def get_guardian_news_today_json(api_key = GUARDIAN_API_KEY):
    """Fetches news articles published today from The Guardian API and returns a JSON object (list of dicts)."""
    today_str = datetime.now().strftime('%Y-%m-%d')
    api_url = f"https://content.guardianapis.com/search"
    params = {
        'api-key': api_key,
        'from-date': today_str,
        'to-date': today_str,
        'show-fields': 'headline,shortUrl,firstPublicationDate', # Specify desired fields
        'page-size': 50 # Adjust as needed
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        articles = []
        if 'response' in data and 'results' in data['response']:
            for item in data['response']['results']:
                articles.append({
                    'title': item.get('webTitle'),
                    'url': item.get('webUrl'),
                    'publication_date': item.get('webPublicationDate'),
                    'headline': item.get('fields', {}).get('headline'),
                    'short_url': item.get('fields', {}).get('shortUrl')
                })
        
        # Return the list of dictionaries directly
        return articles 
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Guardian API: {e}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Newsdata.io API call function

def get_newsdata_news_today_json(api_key = NEWSDATA_API_KEY, language='en', country='us,gb'):
    """Fetches latest news articles from the Newsdata.io API (primarily from today) and returns a JSON object (list of dicts)."""
    # Note: Newsdata.io /latest endpoint gets recent news. Filtering precisely for *today* might require paid plans or post-filtering.
    # We'll fetch recent news and can filter later if needed.
    api_url = "https://newsdata.io/api/1/latest"
    params = {
        'apikey': api_key,
        'language': language,
        # 'country': country, # Free plan might restrict this or number of countries
        # 'timeframe': 24 # Get news from the last 24 hours (check if supported on free plan)
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        articles = []
        if data.get('status') == 'success' and 'results' in data:
            for item in data['results']:
                # Basic filtering for today's date if pubDate is available
                # pub_date_str = item.get('pubDate') # Format is often 'YYYY-MM-DD HH:MM:SS'
                # if pub_date_str:
                #    try:
                #        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S').date()
                #        if pub_date != datetime.now().date():
                #            continue # Skip if not today
                #    except ValueError:
                #        pass # Ignore if date format is unexpected
                        
                articles.append({
                    'title': item.get('title'),
                    'url': item.get('link'),
                    'publication_date': item.get('pubDate'),
                    'description': item.get('description'),
                    'source': item.get('source_id'),
                    'keywords': item.get('keywords'), # Often null on free tier
                    'image_url': item.get('image_url')
                })
        else:
             print(f"Newsdata API did not return success status. Status: {data.get('status')}")
             print(f"Response: {data}") # Print full response for debugging
             return []
        
        # Return the list of dictionaries directly
        return articles 
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Newsdata API: {e}")
        # If the error is due to the response content, print it
        if 'response' in locals() and response is not None:
             print(f"Response status code: {response.status_code}")
             print(f"Response text: {response.text}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []