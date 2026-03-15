from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


import requests
from gtts import gTTS
import os

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "b9bba2edb19db5e5de8ccfda8c5022d4"


# Function to convert temperature from Kelvin to Celsius and Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


# Function to get weather information for a given city
def get_weather(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()

    if response.get('cod') == 200:
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']

        text_response = (f"Temperature in {city}: {temp_celsius:.2f}\u00B0C\n"
                         f"Temperature in {city} feels like: {feels_like_celsius:.2f}\u00B0C\n"
                         f"Humidity in {city}: {humidity}%\n"
                         f"Normal weather in {city}: {description}")


        return text_response
    else:
        return "Sorry, I couldn't fetch the weather information for that location."

# Initialize Twilio client with Twilio API credentials
account_sid = "ACf48bf579d6ca0449165195624c00457c"
auth_token = "121b2025c0d27f5cd843f5a240291183"
client = Client(account_sid, auth_token)

def process_message(message):
    user_input = message.body.lower().strip()
    if user_input == 'exit':
        return "Goodbye!"
    else:
        city = user_input
        response = get_weather(city)
        return response

# Main chat loop
while True:
    user_input = input("Bot: Which city's weather would you like to know? (Type 'exit' to quit)\nYou: ")

    if user_input.lower() == 'exit':
        break

    city = user_input.strip()
    response = get_weather(city)
    print("Bot:", response)
