from os import getenv
import logging

API = getenv('API')
INTERVAL = int(getenv('INTERVAL', '60'))
PER_PAGE = int(getenv('PER_PAGE', '1'))
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
RMQ_HOST = getenv('RMQ_HOST', 'localhost')
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('grab_pexels')
log.setLevel(LOG_LEVEL)

log.info(f'got this vars!\n'
         f'API = {API}\n'
         f'INTERVAL = {INTERVAL}\n'
         f'LOG_LEVEL = {LOG_LEVEL}\n'
         f'RMQ_HOST = {RMQ_HOST}\n'
         f'PER_PAGE = {PER_PAGE}\n')
