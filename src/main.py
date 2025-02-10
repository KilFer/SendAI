import logging
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, Query

from modules import Modules, load_modules
from utils import Cache, log

load_dotenv()
app = FastAPI()
cache = Cache()

loaded_modules = load_modules()

@app.get("/modules")
async def list_modules():
    """
    Returns a list of all available modules.
    """
    return {"modules": [module.value for module in loaded_modules.keys()]}

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
    called_modules = Modules.from_strings(selected_modules)

    response_data = {}

    for called_module in called_modules:
        if called_module in loaded_modules:
            response_data[called_module.value] = cache.get_cached_data(called_module.value, reload, loaded_modules[called_module].get)
        else:
            log(f"ERROR. Module {called_module.value} is not loaded.", logging.WARN)

    return response_data

@app.on_event("startup")
async def startup_event():

    log(f"Loaded modules", logging.INFO)
    log("🚀 Startup complete!", logging.INFO)
