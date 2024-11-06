import logging


def configure_logging(logger_name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    stream_handle = logging.StreamHandler()
    stream_handle.setFormatter(formatter)
    file_handle = logging.FileHandler("shh.log")
    file_handle.setFormatter(formatter)

    logger.addHandler(stream_handle)
    logger.addHandler(file_handle)

    logger.setLevel(logging.DEBUG)

    return logger
