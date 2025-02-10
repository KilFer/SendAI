import logging
from src.config import CONFIG


logger = logging.getLogger(__name__)
loglevel = CONFIG["general"]["log_level"].upper()
logger.setLevel(loglevel)
handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.log(logging.INFO, f"Log level defined as: {loglevel}")

def log(message, level):
    logger.log(level, message)