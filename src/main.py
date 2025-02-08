import logging
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, Query

from modules import News, Weather, Quote, Modules, Ephemerides
from utils import Cache, log

load_dotenv()
app = FastAPI()
cache = Cache()

@app.get("/generate_info")
async def generate_info(
    modules: str = Query(""),
    reload: bool = Query(False)
) -> Dict[str, Any]:
    """
    Generate and return information from selected modules.
    Example usage: /generate_info?modules=news,weather
    """
    log(f"Modules received: {modules}", logging.INFO)
    selected_modules = modules.split(",")
    valid_modules = Modules.from_strings(selected_modules)

    response_data = {}

    # Fetch data from requested modules
    if Modules.NEWS in valid_modules:
        news = News()
        response_data["news"] = cache.get_cached_data("news", reload, news.get)

    if Modules.WEATHER in valid_modules:
        weather = Weather()
        response_data["weather"] = cache.get_cached_data("weather", reload, weather.get)

    if Modules.QUOTE in valid_modules:
        quote = Quote()
        response_data["quote"] = cache.get_cached_data("quote", reload, quote.get)

    if Modules.EPHEMERIDES in valid_modules:
        ephemerides = Ephemerides()
        response_data["ephemerides"] = cache.get_cached_data("ephemerides", reload, ephemerides.get)

    return response_data

# def main():
#
#     load_modules = Modules.from_strings(os.getenv("MODULES_TO_LOAD").split(','))
#
#     print(f"Loading modules: {load_modules}")
#
#     ### NEWS
#     if Modules.NEWS in load_modules:
#         news = News()
#         recent_news = news.get()
#         if recent_news:
#             print("Here are the latest news articles:")
#             for idx, article in enumerate(recent_news, start=1):
#                 print(f"\nArticle {idx}:")
#                 print(f"Title: {article['title']}")
#                 print(f"Description: {article['description']}")
#                 print(f"Read more: {article['url']}")
#         else:
#             print("No news articles available at the moment.")
#         # Del dia anterior hay UN MONTON de Noticias. Filtrar con IA:
#         #  - Descartar noticias de Fútbol
#         #  - Descartar no-noticias (Horóscopos y Santos)
#         #  - Dar importancia a noticias de Zaragoza y Europa
#         #  - Dar importancia a noticias positivas
#
#     ## WEATHER
#     if Modules.WEATHER in load_modules:
#         weather = Weather()
#         current_weather = weather.get()
#         if current_weather:
#             print("\nCurrent Weather:")
#             print(f"Actual temperature: {current_weather['temperature_actual']}°C")
#             print(f"Max Temperature: {current_weather['temperature_max']}°C")
#             print(f"Min Temperature: {current_weather['temperature_min']}°C")
#             print(f"Wind Speed: {current_weather['wind_speed']} km/h")
#             print(f"Precipitation: {current_weather['precipitation']} mm")
#             print(f"Forecast: {current_weather['forecast']}")
#         else:
#             print("Weather data is currently unavailable.")
#
#     ## QUOTE
#     if Modules.QUOTE in load_modules:
#         quote = Quote()
#         current_quote = quote.get()
#         if current_quote:
#             print("\nQuote of the day:")
#             print(f"\"{current_quote['quote']}\"")
#             print(f" - {current_quote['author']}")
#         else:
#             print("Quote of the day is currently unavailable")
#
#     if Modules.EPHEMERIDES in load_modules:
#         ephemerides = Ephemerides()
#         current_ephemerides = ephemerides.get()
#         if current_ephemerides:
#             print("\nEphemerides")
#             if current_ephemerides['events']:
#                 print(" - List of events:")
#                 for event in current_ephemerides['events']:
#                     print(f"    - {event}")
#             if current_ephemerides['births']:
#                 print(" - List of births:")
#                 for birth in current_ephemerides['births']:
#                     print(f"    - {birth}")
#             if current_ephemerides['deaths']:
#                 print(" - List of deaths:")
#                 for death in current_ephemerides['deaths']:
#                     print(f"    - {death}")
#
#
# if __name__ == '__main__':
#     main()