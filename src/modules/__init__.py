import logging
from enum import Enum
from typing import List

from src.modules.news import News
from src.modules.weather import Weather
from src.modules.quote import Quote
from src.modules.ephemerides import Ephemerides
from src.modules.calendar import Calendar
from src.modules.tasks import Tasks
from src.utils import log


class Modules(Enum):
    NEWS = "news"
    WEATHER = "weather"
    QUOTE = "quote"
    EPHEMERIDES = "ephemerides"
    CALENDAR = "calendar"
    TASKS = "tasks"

    @classmethod
    def from_strings(cls, values: List[str]) -> List["Modules"]:
        return [module for module in cls if module.value in values]


def load_modules():
    loaded_modules = {}
    if Tasks.can_be_loaded():
        loaded_modules[Modules.TASKS] = Tasks()
    else:
        log(f"❗ [TASK] module couldn't be loaded.", logging.WARN)
    if News.can_be_loaded():
        loaded_modules[Modules.NEWS] = News()
    else:
        log(f"❗ [NEWS] module couldn't be loaded.", logging.WARN)
    if Weather.can_be_loaded():
        loaded_modules[Modules.WEATHER] = Weather()
    else:
        log(f"❗ [WEATHER] module couldn't be loaded.", logging.WARN)
    if Quote.can_be_loaded():
        loaded_modules[Modules.QUOTE] = Quote()
    else:
        log(f"❗ [QUOTE] module couldn't be loaded.", logging.WARN)
    if Ephemerides.can_be_loaded():
        loaded_modules[Modules.EPHEMERIDES] = Ephemerides()
    else:
        log(f"❗ [EPHEMERIDES] module couldn't be loaded.", logging.WARN)
    if Calendar.can_be_loaded():
        loaded_modules[Modules.CALENDAR] = Calendar()
    else:
        log(f"❗ [CALENDAR] module couldn't be loaded.", logging.WARN)

    log(f"Modules loaded: {[module.value for module in loaded_modules.keys()]}", logging.INFO)
    return loaded_modules