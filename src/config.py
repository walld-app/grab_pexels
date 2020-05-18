from os import getenv
import logging
import pika

API = getenv('API')
INTERVAL = int(getenv('INTERVAL', '60'))
PER_PAGE = int(getenv('PER_PAGE', '1'))
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
RMQ_HOST = getenv('RMQ_HOST', 'localhost')
RMQ_USER = getenv('RMQ_USER', 'guest')
RMQ_PASS = getenv('RMQ_PASS', 'guest')
RMQ_PORT = getenv('RMQ_PORT', '5672')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('grab_pexels')
log.setLevel(LOG_LEVEL)

log.info(f'got this vars!\n'
         f'API = {API}\n'
         f'INTERVAL = {INTERVAL}\n'
         f'LOG_LEVEL = {LOG_LEVEL}\n'
         f'RMQ_HOST = {RMQ_HOST}\n'
         f'RMQ_PORT = {RMQ_PORT}\n'
         f'PER_PAGE = {PER_PAGE}\n')


CREDS = pika.credentials.PlainCredentials(RMQ_USER,
                                          RMQ_PASS,
                                          erase_on_connect=True)
PIKA_PARAMS = pika.ConnectionParameters(host=RMQ_HOST,
                                        port=RMQ_PORT,
                                        credentials=CREDS)
PIKA_DURABLE = pika.BasicProperties(delivery_mode=2)