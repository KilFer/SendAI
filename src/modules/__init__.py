import logging
from enum import Enum
from typing import List, Type

from src.modules.news import News
from src.modules.weather import Weather
from src.modules.quote import Quote
from src.modules.ephemerides import Ephemerides
from src.modules.calendar import Calendar
from src.modules.tasks import Tasks
from src.utils import log


class Modules(Enum):
    NEWS = ("news", News)
    WEATHER = ("weather", Weather)
    QUOTE = ("quote", Quote)
    EPHEMERIDES = ("ephemerides", Ephemerides)
    CALENDAR = ("calendar", Calendar)
    TASKS = ("tasks", Tasks)

    def __init__(self, value: str, module_class: Type):
        self._value_ = value
        self.module_class = module_class

    @classmethod
    def from_strings(cls, values: List[str]) -> List["Modules"]:
        return [module for module in cls if module.value in values]


def load_modules():
    loaded_modules = {}
    for module in Modules:
        if module.module_class.can_be_loaded():
            loaded_modules[module] = module.module_class()
        else:
            log(f"Module {module.value} couldn't be loaded. Check configuration. ", logging.WARN)

    log(f"Modules loaded: {[module.value for module in loaded_modules.keys()]}", logging.INFO)
    return loaded_modules