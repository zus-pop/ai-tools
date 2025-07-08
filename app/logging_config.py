import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

def setup_logging(log_level: str = LogLevel.ERROR):
    log_level = log_level.upper()
    log_levels = [level.value for level in LogLevel]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevel.ERROR)
        return
    
    if log_level == LogLevel.DEBUG:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return
    
    logging.basicConfig(level=log_level)