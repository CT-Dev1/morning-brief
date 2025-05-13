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

3rd section: Classes - This is all the events for someone else. Summarize the events that are upcoming for this person.

4rd section: sunkqj@gmail.com - Ignore this calendar

Format your answer in these 4 sections.

Here is the json calendar data nested by the calendars I've mentioned:

{full_calendars}
"""
client = genai.Client(api_key=GEMINI_API_KEY)

calendar_input = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17", contents = prompt_calendar_parsing
)
print(calendar_input.text)


# %%
# now processing for the emails

prompt_email_processing = f"""

You are meant for mid-level processing of raw data into readable strings of text.
Here is an output of emails in the inbox. You need to select the relevant and important emails based on what isn't spam and what delivers important information based on your judgement. Once you have selected the important emails. Report their information below. You often won't have the full context of the email, so just report al the information that you can. Create a list of relevant emails as a string of text. 

Here is the raw data:

{primary_emails}

"""
email_input = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17", contents = prompt_email_processing
)
print(email_input.text)

# %%

prompt_news_processing = f"""
You are meant for mid-level processing of raw data into readable strings of text.
Here is an output from the guardian newsletter API. You need to distill the headlines of the recent news. You should trim down the news headlines into about 5-6 that you think are particularly important. Prioritize news related to international relations, ukraine war and economics. Report as much information as is available for each of the selected news stories.

Here is the raw API output from the guardian:

{news_headlines}
"""

news_input = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17", contents = prompt_news_processing
)

print(news_input.text)

# %%

from datetime import datetime
now =datetime.now()

prompt_weather_processing = f"""

Your task is to convert a verbose json output from a weather forecast api into a readable weather forecast for the day. Prioritize reporting changes in the weather. For instance, if the cloudiness percentage is the same throughout the day, then just say that, but if it changes a lot, then go into more detail. The same applies to temperature and other metrics. You produce a reasonably large paragraph, give lots of details if it is necessary. Focus particularly on temperature, humidity, weather description (weather_desc), wind speed, precipitation probability (ie. chance of rain). 

Note that the current time is {now}, based your forecast off this starting point.

Here is the raw data output to parse:

{weather_data}
"""

weather_input = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17", contents = prompt_weather_processing
    )

print(weather_input.text)

# %%

# MAIN SCRIPT GENERATION

main_script_prompt = f"""
Your task is to generate a 5 minute spoken script for a morning brief that provides important details for the beginning of the day. It'll be about 800-1000 words.

There are 4 sections to this brief: Email, Calendar, Weather and News. You'll be provided with a section of input text detailing the information of each of these sections.

INTRODUCTION.
You should start the brief by greeting the person. Their name is Ryan. Say things like 'Rise and Shine.' Next, you should provide a short poem, about 5-6 lines long, that relates to a novel insight on the meaning of life. 

Gradually transition into the next sections, which start on the business for the day.

EMAIL:

Parse through the below email text. Combine the information from the emails into a conversational briefing on what is in the inbox. Prioritize recency, the current time is {now}.

{email_input.text}

Remember to close out the section with a calm transition sentence into the next section. 

CALENDAR AND TASKS:

We're gonna have 2 sub-sections for the calendar section. 1) actual upcoming events (includes all calendars that are not to-do). 2) tasks (the to-do calendar).  Your goal is to  report the upcoming events/tasks for each of these. 

Subsection 1 (calendar events):

Report the primary details of any upcoming events. Structure your briefing here by day and time, moving in chronological order. Note that the current time is {now}. Try to infer some event details from any acronyms or short hand used in the calendar descriptions. 

Subsection 2 (tasks):

Report the upcoming tasks here with a similar logic to the calendar events, but note that these are just reminders on what needs to be done soon. 

Here is the input information for both of the above subsections:

{calendar_input.text}

NEWS:

Please report the headlines from below. If you have the capability to search the web for additional news, then please do so. It's ok to be a bit more verbose in this section.

{news_input.text}


WEATHER:

Finally, you should report the weather for the day from the description below. Put emphasis on any important details, particularly temperature and rain probability. No need to make this section too long. 

{weather_input.text}

CONCLUSION:

Conclude with a random quote from a philosopher that is about 1-2 sentences long. It can be on any random topic. Then wish the user a good day.

Notes on tone and style. Your tone throughout should be conversational and friendly, but also accurate and informative. Focus on maintaining accuracy of information provided. Don't say many cliche things like 'remember to bring your umbrella,' focus on being direct but still casual and somewhat conversational. 

"""

main_script = client.models.generate_content(
    model="gemini-2.5-pro-preview-05-06", contents = main_script_prompt
    )

print(main_script.text)

# %%

with open("scripts/main_script.txt", "w") as f:
    f.write(main_script.text)

print("script saved in /scripts")
# %%
