import requests

from good_repr import AttrDisplay

class Picture(AttrDisplay):
    def __init__(self, service, source, author, height, width, url):
        self.service = service
        self.source = source
        self.author = author
        self.height = height
        self.width = width
        self.url = url
        self.colours = None

    @classmethod
    def from_pexel(cls, pexel):
        return cls(service='Pexel',
                   source=pexel.url,
                   author=pexel.photographer,
                   height=pexel.height,
                   width=pexel.width,
                   url=pexel.src['original'])

    def download(self):
        pass

    def calc_colour(self):
        pass
