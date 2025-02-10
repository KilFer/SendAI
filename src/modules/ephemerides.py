import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()

def parse_text(str):
    result = str.replace('&#8211;','–')
    return result

class Ephemerides:

    def __init__(self):
        self.api_url = "https://today.zenquotes.io/api"
        self.filtered_words = os.getenv("EPHEMERIDES_WORDS_FILTERED").split(',')
        self.limit_values = int(os.getenv("EPHEMERIDES_LIMIT_RESULTS"))

    @staticmethod
    def can_be_loaded():
        return True

    def get(self):
        try:

            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json().get('data', {})

            events = data.get('Events', [])
            result_events = []
            for event in events:
                if not self.contains_filtered_words(event['text']):
                    result_events.append(parse_text(event['text']))

            births = data.get('Births', [])
            result_births = []
            for birth in births:
                if not self.contains_filtered_words(birth['text']):
                    result_births.append(parse_text(birth['text']))

            deaths = data.get('Deaths', [])
            result_deats = []
            for death in deaths:
                if not self.contains_filtered_words(death['text']):
                    result_deats.append(parse_text(death['text']))

            result = {
                'events' : self.select_random_values(result_events),
                'births' : self.select_random_values(result_births),
                'deaths' : self.select_random_values(result_deats)
            }

            return result

        except requests.exceptions.RequestException as e:
            print(f"Error fetching quote of the day: {e}")
            return {}


    def select_random_values(self, arr):
        if self.limit_values >= len(arr):
            return arr

        selected = set(random.sample(arr, self.limit_values))
        return [item for item in arr if item in selected]


    def contains_filtered_words(self, str):
        for word in self.filtered_words:
            if word in str:
                return True
        return False