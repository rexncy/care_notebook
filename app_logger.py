import logging
import sys


def get_logger(name, level, write_file=True, write_console=True):
    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if write_file:
        # Configure the file handler
        file_handler = logging.FileHandler(
            "data/care_data_downloader.log", mode="a", encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
            )
        )
        logger.addHandler(file_handler)

    if write_console:
        # Configure the console handler
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
            )
        )
        logger.addHandler(console_handler)

    return logger
