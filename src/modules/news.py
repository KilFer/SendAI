import requests
from datetime import datetime, timedelta

from src.config import CONFIG


def yesterday_date():
    yesterday = datetime.today() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


class News:
    def __init__(self):
        self.api_key = CONFIG["news"]["api_key"]
        self.api_url = 'https://api.worldnewsapi.com/top-news'
        self.country = 'es'
        self.language = 'es'

    @staticmethod
    def can_be_loaded():
        return bool(CONFIG["news"]) and bool(CONFIG["news"]["api_key"])

    def get(self):
        params = {
            'api-key': self.api_key,
            'source-country': self.country,
            'date': yesterday_date(),
            'language': self.language
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            top_news = data.get('top_news', [])

            news_list = []
            for news in top_news:
                article = news.get('news', [])[0]
                number_sources = len(news.get('news', []))
                news_item = {
                    'title': article.get('title'),
                    'description': article.get('summary'),
                    'url': article.get('url'),
                    'image': article.get('image'),
                    'number_sources': number_sources
                }
                news_list.append(news_item)

            return news_list
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []

