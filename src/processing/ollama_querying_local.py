import requests
import json
from src.utils.config import OLLAMA_API_BASE
from src.weather import get_current_weather_zipcode,get_forecast_by_zip_code
from datetime import datetime
from src.email_retrieve.email_collection import get_top_emails_json

class PromptManager:
    """Manages llm prompts for different data types. 
    """
    @staticmethod
    def weather_forecast_prompt(json_data: dict, num_forecasts: int) -> str:
        now = datetime.now()
        return(
        f"Your task is to produce a short paragraph detailing the weather over the next 24 hours from a raw data output in python's dictionary form. The data contains {num_forecasts} forecasts. The current time and date is {now.strftime("%d/%m/%Y, %H:%M:%S")}.Here is the weather data: {json_data}"
        )

    @staticmethod
    def weather_now_prompt(json_data: dict) -> str:
        now = datetime.now()
        return(
            f"Your task is to produce a couple sentences accurately describing the current weather. The current time is {now.strftime("%d/%m/%Y, %H:%M:%S")}. The data is given in python's dictionary form. Here is the weather data: {json_data}"
        )
    
    @staticmethod
    def email_prompt(json_data: dict):
        return(
            f"your task is to summarize top email in my inbox. the emails will be presented to you in a list of dictionaries format, where each dictionary has keys 'id', 'threadId', 'snippet', 'subject', 'from', 'date'. you should produce maximum a couple paragraphs. How to measure importance? 1) Emails that are spam-like, or are verbose, like security alerts or technical updates aren't important. 2) emails that details new meetings, or requests from individuals are important. 3) generally, i receive a lot more useless emails than I do useful ones. What to put in your response? Summarize the inbox emails and mention any questions that they ask in particular, things that I need to follow-up one, action items. Use your judgement. In your output, for the important email, retain as much of their content as possible. There will be {len(json_data)} emails in total. Here are the emails from my inbox: {json_data}"  
        )

def generate_text_ollama(prompt, model="deepseek-r1:latest", options=None):
    """Generate text using specified model"""
    url = f"{OLLAMA_API_BASE}/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    if options:
        payload["options"] = options
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# For direct script testing
if __name__ == "__main__":
    model_name = "deepseek-r1:latest"
    options = None # play around with this later
    num_forecasts = 5
    json_data = get_forecast_by_zip_code('e1','gb',num_forecasts)
    prompt = PromptManager.weather_forecast_prompt(json_data, num_forecasts)
    
    response_weather_now = generate_text_ollama(PromptManager.weather_now_prompt(json_data=get_current_weather_zipcode('e1','gb')),model=model_name, options=options)
    print(response_weather_now)
    
    response_forecast = generate_text_ollama(prompt, model=model_name, options = options)
    print(response_forecast)
    
    email_json = get_top_emails_json()
    email_prompt = PromptManager.email_prompt(json_data=email_json)
    
    response_email = generate_text_ollama(email_prompt, model=model_name, options=options)
    print(response_email)
    
    
    
    
        