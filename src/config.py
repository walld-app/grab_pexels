from os import getenv
import logging

API = getenv('API')
INTERVAL = int(getenv('INTERVAL', '60'))
PER_PAGE = int(getenv('PER_PAGE', '1'))
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
RMQ_HOST = getenv('RMQ_HOST', 'localhost')

log = logging.getLogger('grab_pexels')
log.setLevel(LOG_LEVEL)
