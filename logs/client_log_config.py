import logging
import inspect


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')
handler = logging.FileHandler('logs/client.log', encoding='UTF-8')
formater = logging.Formatter('%(asctime)s %(levelname)-8s module:%(module)s %(message)s')
handler.setFormatter(formater)
logger.addHandler(handler)

def log(func):
    def wrapper(*arg, **kwarg):
        r = func(*arg, **kwarg)
        call_fuction = inspect.stack()[1][3]
        if call_fuction == '<module>':
            logger.info(f'Запуск функции {func.__name__} с аргументами {arg} {kwarg}')
        else:
            logger.info(f'Запуск функции {func.__name__} из функции {call_fuction} с аргументами {arg} {kwarg}')
        return r
    return wrapper

