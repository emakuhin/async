import logging
from logging.handlers import  TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('server')
formater = logging.Formatter('%(asctime)s %(levelname)-8s module:%(module)s %(message)s')
handler = TimedRotatingFileHandler('logs/server.log', encoding='UTF-8', when='midnight', interval=1)
handler.setFormatter(formater)
log.addHandler(handler)



