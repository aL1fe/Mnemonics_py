import logging


class CustomFormatter(logging.Formatter):
    white = "\033[37m"
    green = "\033[32m"
    yellow = "\033[33m"
    cyan = "\033[36m"
    red = "\033[91m"
    reset = "\033[0m"

    LOG_FORMAT = ("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)")

    FORMATS = {
        logging.DEBUG: white + LOG_FORMAT + reset,
        logging.INFO: green + LOG_FORMAT + reset,
        logging.WARNING: yellow + LOG_FORMAT + reset,
        logging.ERROR: cyan + LOG_FORMAT + reset,
        logging.CRITICAL: red + LOG_FORMAT + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.LOG_FORMAT)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
