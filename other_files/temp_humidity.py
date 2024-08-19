import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("weather_api_key")
# Define the city and URL
city = 'Mumbai'
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    rounded_temperature = int(round(temperature, 1)) # Round to 1 decimal place
    rounded_humidity = int(round(humidity, 1))

    print(f'Temperature in {city}: {rounded_temperature}°C')
    print(f'Humidity in {city}: {rounded_humidity}%')
else:
    print('Failed to retrieve data:', response.status_code)

