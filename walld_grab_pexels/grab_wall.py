from time import sleep

from pypexels import PyPexels
from pypexels.src.errors import PexelsError
from walld_db.helpers import DB, Rmq
from walld_db.models import PictureValid

from config import (API, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, INTERVAL,
                    PER_PAGE, RMQ_HOST, RMQ_PASS, RMQ_PORT, RMQ_USER, log)


def do_stuff(infinite=True):

    db = DB(host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            passwd=DB_PASS,
            name=DB_NAME)

    rmq = Rmq(host=RMQ_HOST,
              port=RMQ_PORT,
              user=RMQ_USER,
              passw=RMQ_PASS)

    pexel = PyPexels(api_key=API)

    log.info('started')

    banned = False
    while True:
        try:
            log.info('Attempting to get photos!')
            entries = set(pexel.random(per_page=PER_PAGE).entries)
            banned = False

        except PexelsError:
            word = "Still" if banned else "Got"
            log.warning(f'{word} banned on pexels, waiting 5 min.')
            banned = True
            for _ in range(6):
                rmq.connection.process_data_events()
                sleep(50)
            continue

        rejected_pics = db.seen_pictures

        for photo in entries:
            source = photo.src["original"]
            if source in rejected_pics:
                log.info(f'Already seen this({source}) picture!')
                continue

            db.add_seen_pic(source)

            pic = PictureValid(service="Pexels",
                               download_url=photo.src["original"],
                               preview_url=photo.src["large"],
                               source_url=photo.url,
                               height=int(photo.height),
                               width=int(photo.width))

            if photo.height > photo.width:
                log.info('not adding this pic because height > weight, for now')
                log.debug(f' height = {photo.height}\nwidth={photo.width}')
                continue

            log.info(f'Adding {pic}!')

            rmq.channel.basic_publish(exchange='',
                                      routing_key='check_out',
                                      body=pic.json(),
                                      properties=rmq.durable)

        if not infinite:
            return

        int_range = range(0, INTERVAL, 20)
        for _ in int_range:
            how_many = len(list(int_range))
            rmq.connection.process_data_events()
            sleep(INTERVAL/how_many)
