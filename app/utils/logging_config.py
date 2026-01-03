import logging
import logging.handlers
import queue
from app.utils.custom_log_formatter import CustomFormatter


def setup_logging(log_file: str = "app.log"):
    log_queue = queue.Queue(-1)

    # --- Queue handler ---
    queue_handler = logging.handlers.QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(queue_handler)

    # --- Console handler (colors) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # console log level
    console_handler.setFormatter(CustomFormatter())

    # --- File handler (no colors) ---
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)  # file log level
    file_handler.setFormatter(logging.Formatter(CustomFormatter().LOG_FORMAT))

    # --- Queue listener ---
    listener = logging.handlers.QueueListener(
        log_queue,
        console_handler,
        file_handler,
        respect_handler_level=True,
    )

    listener.start()
    return listener
