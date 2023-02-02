
from bs4 import BeautifulSoup
import json
import requests
import plyer
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def weather(city):
    city = city.replace(" ", "+")
    try:
        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        print("Searching...\n")
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        with open("weadata.json", "r") as file:
            data = json.load(file)
        num  = data["num"]
        data["num"] = num + 1
        with open("weadata.json",  "w") as file:
            json.dump(data ,file, indent=4)


        # print(location)
        # print(time)
        # print(info)
        # print(weather+"°C")
        plyer.notification.notify(
            title = "Todays Weather",
            message = "City : " + location +"\nWeather : " + weather + "°C, " + info ,
            app_icon = None,
        )                                                                                               
        speak(f"Hello  sir, Todays   weather   updates   of {location} are")

        speak(f"Temperature  in  jodhpur is {weather}°Celsius And  I  think  it  {info} outside")
    except:
        plyer.notification.notify(
        title = "Todays Weather",
        message = "No internet",
        app_icon = None,) 
    

with open("weadata.json", "r") as file:
    datu = json.load(file)
if datu["num"] == 0 and datu["city"] == "":
    city1 = input('Enter the Name of City ->')
    city = city1 + " weather"
    weather(city)

    datu["city"] = city1
    with open("weadata.json", "w") as file:
        json.dump(datu , file)
else:
    weather(datu["city"] + "weather")


