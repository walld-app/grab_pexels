from time import sleep

import pika
from pypexels import PyPexels

from config import API, INTERVAL, PER_PAGE, PIKA_DURABLE, PIKA_PARAMS, log
from picture import Picture, PictureValid


def prepare_stuff():
    connection = pika.BlockingConnection(PIKA_PARAMS)
    channel = connection.channel()
    channel.queue_declare(queue='check_out', durable=True)
    return channel

def start_grab():
    chan = prepare_stuff()
    pexel = PyPexels(api_key=API)
    wait = 0
    log.info('started')
    while True:
        log.info('Attemting to get photos!')
        try:
            random_photos_page = pexel.random(per_page=PER_PAGE)
        except: # TODO В либе прокол по ходу и мы не можем отследить ошибку
            log.warning(f'Got banned from pexels,'
                        f' waiting {str(INTERVAL + wait)} secs.')
            sleep(INTERVAL + wait)
            wait += 30
            continue
        wait = 0
        for photo in random_photos_page.entries:
            pic = PictureValid(service="Pexels",
                               download_url=photo.src["original"],
                               preview_url=photo.src["large"],
                               author=photo.photographer,
                               **photo.__dict__)
            # добавить проверку на повторение с помощью постгре
            log.info(f'Adding {pic}!')
            chan.basic_publish(exchange='',
                               routing_key='check_out',
                               body=pic.json(),
                               properties=PIKA_DURABLE)
        sleep(INTERVAL)
