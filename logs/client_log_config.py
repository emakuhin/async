import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('client')
handler = logging.FileHandler('logs/client.log', encoding='UTF-8')
formater = logging.Formatter('%(asctime)s %(levelname)-8s module:%(module)s %(message)s')
handler.setFormatter(formater)
log.addHandler(handler)