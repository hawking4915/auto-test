from method.out_log import logger

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as f:
            logger.info("%s Exception: %s." % (func.__name__, f))
            result = 'False'
            return result
    return wrapper