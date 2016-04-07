
from .base import EngineBase


class GoogleEngine(EngineBase):
    def __init__(self):
        super(GoogleEngine, self).__init__()
        self.method = 'GET'
        self.name = 'google'
        self.url = 'https://www.google.com/search'
        self.num_per_page = 10

    def set_search(self, search=None, page=0):
        self.data['q'] = search
        self.data['start'] = page * self.num_per_page
