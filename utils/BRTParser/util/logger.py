#coding=utf8

import logging
default_fmt="[%(asctime)s %(levelname)s %(filename)s:%(lineno)d] %(message)s"
default_level = logging.DEBUG

log_warn = logging.WARNING
log_erro = logging.ERROR

logging.basicConfig(format=default_fmt, level=default_level)

def get_logger(name=None, level=default_level, fmt=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if fmt is not None:
        for h in logger.handlers:
            h.setFormatter(logging.Formatter(fmt))
    return logger

