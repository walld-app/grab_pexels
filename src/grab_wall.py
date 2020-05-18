from pickle import dumps
from time import sleep

import pika
from pypexels import PyPexels

from config import API, INTERVAL, PER_PAGE, RMQ_HOST, log
from picture import Picture

def prepare_stuff():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='check_out', durable=True)
    return channel

def start_grab():
    durable = pika.BasicProperties(delivery_mode=2)
    chan = prepare_stuff()
    pexel = PyPexels(api_key=API)
    wait = 0
    while True:
        log.info('Attemting to get photos!')
        try:
            random_photos_page = pexel.random(per_page=PER_PAGE)
        except: # TODO В либе прокол по ходу и мы не можем отследить ошибку
            print(f'Got banned from pexels,'
                  f' waiting {str(INTERVAL + wait)} secs.')
            sleep(INTERVAL + wait)
            wait += 30
            continue
        wait = 0
        for photo in random_photos_page.entries:
            pic = Picture.from_pexel(photo)
            dump = dumps(pic)
            print(f'Adding {pic}!')
            chan.basic_publish(exchange='',
                               routing_key='check_out',
                               body=dump,
                               properties=durable)
        sleep(INTERVAL)
