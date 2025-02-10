import os
from enum import Enum

import requests
from dotenv import load_dotenv

load_dotenv()


class Weather:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.location = os.getenv('WEATHER_LOCATION')
        self.api_url = 'https://www.meteosource.com/api/v1/free/point'

    @staticmethod
    def can_be_loaded():
        return bool(os.getenv('WEATHER_API_KEY')) and bool(os.getenv('WEATHER_LOCATION'))

    def get(self):
        params = {
            'key': self.api_key,
            'place_id': self.location,
            'sections': 'current,daily',
            'units': 'metric',
            'language': 'en'
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            current_weather = data.get('current', {})
            daily_weather = data.get('daily', {}).get('data', [])[0]
            weather_info = {
                'temperature_actual': current_weather.get('temperature'),
                'temperature_max': daily_weather.get('all_day', {}).get('temperature_max'),
                'temperature_min': daily_weather.get('all_day', {}).get('temperature_min'),
                'wind_speed': daily_weather.get('all_day', {}).get('wind', {}).get('speed', {}),
                'precipitation': current_weather.get('all_day', {}).get('precipitation', {}).get('total'),
                'forecast': daily_weather.get('summary'),
                'icon': daily_weather.get('icon')
            }
            return weather_info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return {}


class WeatherIcon(Enum):
    # List of icons (and set of icons): https://www.meteosource.com/documentation#description
    NOT_AVAILABLE = 1
    SUNNY = 2
    MOSTLY_SUNNY = 3
    PARTLY_SUNNY = 4
    MOSTLY_CLOUDY = 5
    CLOUDY = 6
    OVERCAST = 7
    OVERCAST_LOW_CLOUDS = 8
    FOG = 9
    LIGHT_RAIN = 10
    RAIN = 11
    POSSIBLE_RAIN = 12
    RAIN_SHOWER = 13
    THUNDERSTORM = 14
    LOCAL_THUNDERSTORM = 15
    LIGHT_SNOW = 16
    SNOW = 17
    POSSIBLE_SNOW = 18
    SNOW_SHOWER = 19
    RAIN_AND_SNOW = 20
    POSSIBLE_RAIN_AND_SNOW = 21
    LOCAL_RAIN_AND_SNOW = 22
    FREEZING_RAIN = 23
    POSSIBLE_FREEZING_RAIN = 24
    HAIL = 25
    NIGHT_CLEAR = 26
    NIGHT_MOSTLY_CLEAR = 27
    NIGHT_PARTLY_CLEAR = 28
    NIGHT_MOSTLY_CLOUDY = 29
    NIGHT_CLOUDY = 30
    NIGHT_OVERCAST_LOW_CLOUDS = 31
    NIGHT_RAIN_SHOWER = 32
    NIGHT_LOCAL_THUNDERSTORM = 33
    NIGHT_SNOW_SHOWER = 34
    NIGHT_RAIN_AND_SNOW = 35
    NIGHT_POSSIBLE_FREEZING_RAIN = 36