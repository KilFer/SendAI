import requests

class Quote:
    def __init__(self):
        self.api_url = 'https://zenquotes.io/api/today'

    def get(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            quote = response.json()[0]
            quote_info = {
                'quote': quote.get('q'),
                'author': quote.get('a')
            }
            return quote_info

        except requests.exceptions.RequestException as e:
            print(f"Error fetching quote of the day: {e}")
            return {}
