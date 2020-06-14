from time import sleep

from pypexels import PyPexels
from pypexels.src.errors import PexelsError
from walld_db.helpers import Rmq, DB
from walld_db.models import PictureValid, RejectedPicture

from config import (API, INTERVAL, PER_PAGE, RMQ_HOST, RMQ_PASS, RMQ_PORT,
                    RMQ_USER, log, DB_HOST, DB_NAME, DB_PASS, DB_USER, DB_PORT)

def start_grab():

    db = DB(db_host=DB_HOST,
            db_port=DB_PORT,
            db_user=DB_USER,
            db_passwd=DB_PASS,
            db_name=DB_NAME)

    rmq = Rmq(host=RMQ_HOST, port=RMQ_PORT, user=RMQ_USER, passw=RMQ_PASS)

    pexel = PyPexels(api_key=API)
    log.info('started')
    while True:
        log.info('Attemting to get photos!')

        try:
            random_photos_page = pexel.random(per_page=PER_PAGE)
        except PexelsError:
            log.warning(f'Got banned from pexels,'
                        f' waiting 5 mins.')
            sleep(300)
            continue
        entries = list(random_photos_page.entries)
        rpics = db.rejected_pictures
        for photo in entries:
            if photo.src["original"] in rpics:
                rpics.remove(photo.src["original"])

        for photo in entries:
            pic = PictureValid(service="Pexels",
                               download_url=photo.src["original"],
                               preview_url=photo.src["large"],
                               author=photo.photographer,
                               **photo.__dict__)
            log.info(f'Adding {pic}!')
            rmq.channel.basic_publish(exchange='',
                                      routing_key='check_out',
                                      body=pic.json(),
                                      properties=rmq.durable)
        rmq.connection.process_data_events()
        print(db.rejected_pictures)
        sleep(INTERVAL)
