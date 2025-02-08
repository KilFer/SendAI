from enum import Enum
from typing import List

from src.modules.news import News
from src.modules.weather import Weather
from src.modules.quote import Quote
from src.modules.ephemerides import Ephemerides

class Modules(Enum):
    NEWS = "news"
    WEATHER = "weather"
    QUOTE = "quote"
    EPHEMERIDES = "ephemerides"

    @classmethod
    def from_strings(cls, values: List[str]) -> List["Modules"]:
        return [module for module in cls if module.value in values]