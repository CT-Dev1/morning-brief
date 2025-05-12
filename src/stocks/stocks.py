import requests
import json
import os
import sys
# do the sys path append hack for the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load in .env variables from config (api keys)
from src.utils.config import ALPHA_VANTAGE_API_KEY

# See documentation for the stock market API (Alpha Vantage) - https://www.alphavantage.co/documentation/

# Consider making versions of the base functions below for tailored use-cases

# Firstly The time series daily API - covers daily opening/closing prices

def get_daily_time_series(ticker_sym: str):
    """Get daily stock prices for the ticker symbol for the past 4 months. Can be parsed further to isolate specific dates and price changes. Returns a raw json data response. 
    Can be filtered to get specific dates. 

    Args:
        ticker_sym (str): ticker symbol for stock      
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker_sym}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

#print(get_daily_time_series("NVDA"))

# Secondly the intra-day price retrieval API - covers minute-by-minute prices and extended hours trading

def get_intraday_time_series(ticker_sym: str):
    """ Get historical intraday stock prices for the ticker symbol. Get most of the 5 minute time stamps for the previous trading day. Returns raw json data response.
    Can be filtered to get specific times of day.
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker_sym}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

print(get_intraday_time_series("NVDA"))
