from google.cloud import aiplatform

# good source - https://cloud.google.com/python/docs/reference/aiplatform/latest

'''
# this script will eventually house models for low-mid tier processing of json outputs using local and cheap remote llms

# ideas right now include:
- Data Processor class with class methods that include custom prompts for  


something like:

class DataProcessor:
    def __init__(self, local_llm, premium_llm):
        self.local_llm = local_llm
        self.premium_llm = premium_llm
        self.templates = {}
    
    def process_weather(self, json_data):
        prompt = f"Summarize this weather data: {json_data}"
        return self.local_llm.generate(prompt)
    
    def process_emails(self, json_data):
        # Similar processing for emails
        pass

- This way we can customize the local llm prompts for low-level processing to natural language of the different data types

'''


