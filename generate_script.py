# %%

import json
from google import genai
from src.utils.config import GEMINI_API_KEY

# %%
# Load in the data from the collect_data.py script

# Weather data
with open('data/weather_data.json', 'r') as f:
    weather_data = json.load(f)

# news headlines
with open('data/news_headlines.json', 'r') as f:
    news_headlines = json.load(f)

# primary emails
with open('data/primary_emails.json', 'r') as f:
    primary_emails = json.load(f)

# all calendars
with open('data/full_calendars.json', 'r') as f:
    full_calendars = json.load(f)

# Run a test query on a smaller model
# %%

# mid-tier processing

prompt_calendar_parsing = f"""
You are meant for mid-level processing of raw data into readable strings of text.
Here is an output of upcoming events over the next 3 days for a set of google calendars. You need to digest them into their relevant information. Create 4 sections to your response. Each section should detail all the events including date and time and any other information for each event.

1st section: The primary, work, personal, running and fitness, professional development calendars are all upcoming  events for me.

2nd section: To-Do (task-based) - this calendar stores reminders for tasks that I need to do in the future. Summarize my upcoming to-dos in this section

3rd section: Classes - This is all the events for someone else named Emilie. Summarize the events that are upcoming for this person.

4rd section: sunkqj@gmail.com - This is all the events for someone else named Joyce. Summarize the events that are upcoming for this person.

Format your answer in these 4 sections.

Here is the json calendar data nested by the calendars I've mentioned:

{full_calendars}
"""
client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17", contents = prompt_calendar_parsing
)
print(response.text)

# Generate a script for the prompt

# %%
