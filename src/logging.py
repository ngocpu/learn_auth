from enum import Enum
import logging

LOG_FORMATTER = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

class LogLevels(str, Enum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"
    
def config_logging(log_level:LogLevels = LogLevels.error):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]
    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMATTER)
        return

    logging.basicConfig(level=log_level)