import os
import openai
from key import apikey
openai.api_key = os.getenv(apikey)

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
import datetime
from key import apikey
import random

speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatstr = ""

def chat(query):
    global chatstr
    chatstr += f"User: {query}\n Jarvis: "
    print(chatstr)
    openai.api_key = apikey

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    reply = response.choices[0].text.strip()
    speaker.Speak(reply)
    chatstr += f"{reply}\n"
    return reply

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception as e:
        return "Some Error has Occurred. Sorry"

if __name__ == '__main__':
    speaker.Speak("Hello, I am Jarvis")
    while True:
        text = takeCommand()
        speaker.Speak(text)
        
        if "open youtube" in text.lower():
            webbrowser.open("https://youtube.com")
            speaker.Speak("Opening Youtube...")
        
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"], ["google", "https://www.google.com"]]
        
        for site in sites:
            if f"open {site[0]}".lower() in text.lower():
                speaker.Speak(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        elif "open music" in text.lower():
            musicPath = "path"
            os.startfile(musicPath)
            # os.system(f"open {musicPath}")

        elif "the time" in text.lower():
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"The time is {time}")

        elif "open vs code" in text.lower():
            os.system("code")  # Updated the command to open VS Code

        elif "open ai" in text.lower() or "using ai" in text.lower():
            ai(prompt=text)

        else:
            chat(text)
