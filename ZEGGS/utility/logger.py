# logger_config.py
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('LogZeroEGGS')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler('LogZeroEGGS.log', maxBytes=1024*1024, backupCount=5)
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)