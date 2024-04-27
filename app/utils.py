import logging

def getLogger(name: str) -> logging.Logger:
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.ERROR)
    fh = logging.handlers.RotatingFileHandler('error.log', mode='a', maxBytes = 100*1024, backupCount = 3)
    formatter = logging.Formatter(
        "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
    )
    fh.setLevel(logging.ERROR)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger