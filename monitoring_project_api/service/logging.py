"""Logging handler"""

import logging
from pathlib import Path

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(
        *,
        name: str,
        log_file: Path,
        level: int = logging.INFO
) -> None:
    """
    Function used to set up a new logger
    :param name: The name of the logger
    :type name: str
    :param log_file: The path to the log file
    :type log_file: Path
    :param level: The level of the logger
    :type level: logging.Logger
    :return: A new configured logger
    :rtype: logging.Logger
    """
    # Set up handler
    handler = logging.FileHandler(str(log_file))
    handler.setFormatter(formatter)

    # Set up a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
