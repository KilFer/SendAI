import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
loglevel = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(loglevel)
handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.log(logging.INFO, f"Log level defined as: {loglevel}")

def log(message, level):
    logger.log(level, message)