import logging
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Sets up and returns a logger for the given name.
    Ensures consistent logging formatting for the entire framework.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
