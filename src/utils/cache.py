import logging
import time
from .logger import log
from ..config import CONFIG


class Cache:

    def __init__(self):
        self.cache = {}
        self.caching_time = int(CONFIG["general"]["caching_time"])
        log( f"Cache defined as {self.caching_time} seconds", logging.INFO)

    def get_cached_data(self, module_name: str, reload: bool, fetch_func):
        """Retrieve cached data if available and valid; otherwise, refresh."""
        current_time = time.time()
        cache_entry = self.cache.get(module_name)

        if not reload and cache_entry:
            data, timestamp = cache_entry
            if current_time - timestamp < self.caching_time:  # Cache valid for 1 min
                log(f"Getting '{module_name}' data from cache", logging.DEBUG)
                return data

        # Refresh the cache
        log(f"Getting '{module_name}' data from real time", logging.DEBUG)
        new_data = fetch_func()
        self.cache[module_name] = (new_data, current_time)
        return new_data
