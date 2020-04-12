from logging import Formatter, StreamHandler, getLogger


def get_logger(level: str = "INFO"):
    assert type(level) == str
    logger = getLogger()
    logger.setLevel(level)
    handler = StreamHandler()
    handler.setLevel(level)
    formatter = Formatter("[%(asctime)s][%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
