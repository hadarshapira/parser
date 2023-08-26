import os
import logging
import datetime
import tempfile


def init_logger(output_dir: str = tempfile.gettempdir(), name: str = "parser") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    timestamp = datetime.datetime.utcnow().isoformat().replace(':', '_')
    file_handler = logging.FileHandler(os.path.join(output_dir, f"parser_{timestamp}.log"))
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def remove_handlers(logger: logging.Logger):
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
