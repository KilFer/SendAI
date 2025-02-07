from enum import Enum

from src.modules.news import News
from src.modules.weather import Weather
from src.modules.quote import Quote
from src.modules.ephemerides import Ephemerides

class Modules(Enum):
    NEWS = "News"
    WEATHER = "Weather"
    QUOTE = "Quote"
    EPHEMERIDES = "Ephemerides"