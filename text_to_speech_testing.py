
## FIRST TEST - psttsx3 package - local text to speech engine

# %%
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Text to be spoken
text = "Hello! Welcome to the Python text-to-speech tutorial."

# Customize the speech properties

# SPEECH RATE
rate = engine.getProperty('rate')
print(f"Current speech rate: {rate}")

# Set new speech rate
engine.setProperty('rate', 200)  # Adjust as needed

# VOLUME
# Get current volume level
volume = engine.getProperty('volume')
print(f"Current volume level: {volume}")

# Set new volume level
engine.setProperty('volume', 0.9)  # Adjust as needed

# Get available voices
# Get available voices
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name}")

# Set desired voice
engine.setProperty('voice', voices[0].id)  # Change index as needed


# Queue the text for speaking
engine.say(text)

# Process and output the speech
engine.runAndWait()


#voices = engine.getProperty('voices')

# List available voices



## TEST 2 - Google cloud text to speech
# %%
import os
from google.cloud import texttospeech
#import pygame
import time


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "G:/My Drive/DS Projects/tree_builder/home-pc-apis-6b28d2eb69ee.json"

# Simple test of the text to speech interface

"""Converts text to speech using Google Cloud Text-to-Speech API
    
    Args:
        text: The text to convert to speech
        output_file: The output audio file path
        language_code: The language code (e.g., 'en-US', 'es-ES')
        voice_name: The voice to use (e.g., 'en-US-Standard-A')
        speaking_rate: The speaking rate (1.0 is normal, 0.5 is half speed, 2.0 is double)
        pitch: The pitch (-20.0 to 20.0, 0.0 is normal)
        
    Returns:
        Path to the output audio file
"""

text_to_add = '''So I was checking out the infinite chicken farm you made in minecraft. All I can say, is WOW. 
Your skills are just next-level. What the heck man?!

'''

# Initialize the client
client = texttospeech.TextToSpeechClient()

# set the text input
synthesis_input = texttospeech.SynthesisInput(text=text_to_add)

# Set the voice parameters
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Chirp3-HD-Achernar"
)

# Set audio parameters
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate = 1.0,
    pitch = 0.0
)

# Perform text to speech request
response = client.synthesize_speech(
    input = synthesis_input,
    voice = voice,
    audio_config = audio_config
)

output_file = "voice_output.mp3"

# %%
# Write the response to the output file
with open(output_file, "wb") as out:
    out.write(response.audio_content)
    print(f'Audio content written to file "{output_file}"')     

# %%

# Play the audio file using pygame
# Initialize pygame mixer
pygame.mixer.init()

try:
    # Load and play the audio file
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
except Exception as e:
    print(f"Error playing audio: {e}")
finally:
    pygame.mixer.quit()
    

# %%
