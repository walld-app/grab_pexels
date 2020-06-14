from os import getenv
import logging

API = getenv('API')
assert API
INTERVAL = int(getenv('INTERVAL', '120'))
PER_PAGE = int(getenv('PER_PAGE', '20'))
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
RMQ_HOST = getenv('RMQ_HOST', 'localhost')
RMQ_USER = getenv('RMQ_USER', 'guest')
RMQ_PASS = getenv('RMQ_PASS', 'guest')
RMQ_PORT = getenv('RMQ_PORT', '5672')
DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', '5432')
DB_NAME = getenv('DB_NAME', 'postgres')
DB_USER = getenv('DB_USER', 'postgres')
DB_PASS = getenv('DB_PASS', '1234')
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
