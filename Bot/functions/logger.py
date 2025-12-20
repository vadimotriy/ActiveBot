import logging


# Логгер
def setup_logger():
    logger = logging.getLogger("MyBot")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Задаем формат логов
    formatter = logging.Formatter("\033[4m\033[1m\033[32m%(levelname)s\033[0m - %(asctime)s - %(name)s - %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


logger = setup_logger()