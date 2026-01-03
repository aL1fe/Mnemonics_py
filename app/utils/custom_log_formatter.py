import logging


class CustomFormatter(logging.Formatter):
    white = "\033[37m"
    green = "\033[32m"
    yellow = "\033[33m"
    cyan = "\033[36m"
    red = "\033[31m"
    red_light = "\033[91m"
    blue_light = "\033[94m"
    reset = "\033[0m"

    # LOG_FORMAT = ("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d - %(funcName)s)")
    LOG_FORMAT = ("%(asctime)s %(name)s|%(funcName)s %(levelname)s - %(message)s")

    FORMATS = {
        logging.DEBUG: blue_light + LOG_FORMAT + reset,
        logging.INFO: green + LOG_FORMAT + reset,
        logging.WARNING: yellow + LOG_FORMAT + reset,
        logging.ERROR: red + LOG_FORMAT + reset,
        logging.CRITICAL: red_light + LOG_FORMAT + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.LOG_FORMAT)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
