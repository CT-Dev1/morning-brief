# import functions from news script
from .news import get_newsdata_news_today_json, get_guardian_news_today_json

# initialize the functions on loading the module
__all__ = ['get_newsdata_news_today_json', 'get_guardian_news_today_json']
