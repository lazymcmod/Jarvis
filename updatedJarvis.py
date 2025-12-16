import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import os
import requests



API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY LOADED:", API_KEY is not None)







def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.setProperty("rate",170)

    engine.say(audio)
    engine.runAndWait()
    

def command():   
    content = " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio)
            print("you said......... " + content)
        except Exception as e:
            print("Please try again......")

    return content 

def ask_ai(question):
    if not API_KEY:
        return "API key not loaded properly."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        data = response.json()

        print("RAW AI RESPONSE:", data)

        if "choices" not in data:
            return "AI service error or quota exceeded."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI Exception:", e)
        return "Sorry, I am having trouble connecting to AI."




def main_process():    
    while True:
        request = command().lower()
        if "hello" in request:
            speak("Welcome sir, How may i help you")
        elif "play music" in request:
            speak("playing music")
            songs = random.randint(1,3)
            if songs == 1:
                webbrowser.open("https://www.youtube.com/watch?v=uuCFRaFWjwY&list=RDuuCFRaFWjwY&start_radio=1&pp=ygUJYW1wbGlmaWVyoAcB")
            elif songs == 2:
                webbrowser.open("https://www.youtube.com/watch?v=JOX09U8noOE&list=RDJOX09U8noOE&start_radio=1&pp=ygURcGF0YSBjaGFsZWdhIHNvbmegBwE%3D")
            elif songs == 3:
                webbrowser.open("https://www.youtube.com/watch?v=JYodEWUdIso&list=RDJYodEWUdIso&start_radio=1&pp=ygULYmV3YWZhIHNvbmegBwE%3D") 

        elif "time" in request:
           now_time = datetime.datetime.now().strftime("%H:%M")
           speak("Current time is"+ str(now_time))
        elif "date" in request:
            now_time = datetime.datetime.now().strftime("%d:%m")
            speak("Current date is "+ str(now_time)) 
        elif "open google" in request:
            speak("opening google")
            webbrowser.open("https://google.com")
        elif "open youtube" in request:
            speak("opening youtube")
            webbrowser.open("https://youtube.com")
        elif "open github" in request:
            speak("opening github")
            webbrowser.open("https://github.com//")   
        elif "open insta" in request:
            speak("opening insta")
            webbrowser.open("https://www.instagram.com/")  
        elif "open twitter" in request:
            speak("opening twitter")
            webbrowser.open("https://x.com/home") 
        elif "open linkedin" in request:
            speak("opening linkedin")
            webbrowser.open("https://www.linkedin.com/in/ayush-singh-6a660036a/")             
        elif "task" in request:
            task = request.replace("new task","")
            task = task.strip()
            if task != "":
                speak("Adding task: " + task)
                with open ("todo.txt","a") as file:
                    file.write(task + "\n")
        elif "speak work" in request:
            with open ("todo.txt","r") as file:
                  speak("work we have to do today is: " + file.read())
        elif "today work" in request:
            with open ("todo.txt","r") as file:
                  tasks = file.read()
            notification.notify(
                    title = "Today's work",
                    message = tasks
                )  
        elif "open" in request:
            query = request.replace("open", "")
            speak("opening" + query)
            pyautogui.press("super")  
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search wikipedia ", "")
            print(request)
            result = wikipedia.summary(request, sentences=2) 
            speak(result)
        elif "search google" in request:
            request = request.replace("jarvis ", "")
            request = request.replace("search google ", "")
            webbrowser.open("https://www.google.com/search?q=" + request)
        else:
            # Agar koi predefined command match nahi hui
            speak("Let me think")
            answer = ask_ai(request)
            speak(answer)

      
       
    

main_process()    