
from .base import EngineBase


class GoogleEngine(EngineBase):
    def __init__(self, **kwargs):
        super(GoogleEngine, self).__init__(**kwargs)
        self.name = 'google'
        self.url = 'https://www.google.com/search'
        self.page_key = 'start'
        self.search_key = 'q'

    def _findMatchTags(self, soup):
        return soup.find_all('div', class_='rc')

    def _findMatchTitle(self, tag):
        h2 = tag.find('h3')
        return h2.text

    def _findMatchUrl(self, tag):
        h2 = tag.find('h3')
        a = h2.find('a')
        return a.attrs.get('href', '')
