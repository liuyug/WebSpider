
from .base import EngineBase


class BingEngine(EngineBase):
    def __init__(self):
        super(BingEngine, self).__init__()
        self.method = 'GET'
        self.name = 'bing'
        self.url = 'http://www.bing.com/search'
        self.num_per_page = 10

    def set_search(self, search=None, page=0):
        self.data['q'] = search
        self.data['first'] = page * self.num_per_page
