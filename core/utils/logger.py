import logging.config
from logging.handlers import TimedRotatingFileHandler

from utils.logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('quest_bot', when='d', interval=1)
logger.addHandler(handler)
