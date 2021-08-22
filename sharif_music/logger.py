"""logger for project."""
from logging import Formatter
from logging import getLogger
from logging import INFO
from logging import Logger
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import os
from socket import gethostname
from time import time

LOG_CONSOLE: bool = True
LOG_FOLDER: str = f"/var/tmp/logs/{__package__}_{int(time())}"
LOG_LOCATION: str = f"{LOG_FOLDER}/{__package__}.log"
LOG_FORMAT: str = (
    f"%(asctime)s {gethostname()} %(levelname)s %(filename)s:%(lineno)d %(name)s "
    f"%(funcName)s() %(processName)s:%(process)d  %(threadName)s:%(thread)d %(message)s"
)
LEVEL = INFO


def get_logger(name: str) -> Logger:
    """Get a logger with given name."""
    os.makedirs(LOG_FOLDER, exist_ok=True)
    logger = getLogger(name)
    logger.setLevel(LEVEL)
    log_handler = RotatingFileHandler(
        LOG_LOCATION, maxBytes=50 * 1024 * 1024, backupCount=5
    )
    log_handler.setFormatter(Formatter(LOG_FORMAT))
    logger.addHandler(log_handler)

    if LOG_CONSOLE:
        console_handler = StreamHandler()
        console_handler.setLevel(LEVEL)
        console_handler.setFormatter(Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger
