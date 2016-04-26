

from six.moves.urllib.parse import urljoin

from .base import EngineBase


class GoogleEngine(EngineBase):
    def __init__(self, **kwargs):
        self.name = 'google'
        self.firstPage = 'https://www.google.com/ncr'
        super(GoogleEngine, self).__init__(**kwargs)
        self.url = 'https://www.google.com/search'
        self.search_key = 'q'
        self.data['ie'] = 'utf-8'
        self.data['oe'] = 'utf-8'

    def _findMatchTags(self, soup):
        return soup.find_all('div', class_='rc')

    def _findMatchTitle(self, tag):
        h2 = tag.find('h3')
        return h2.text

    def _findMatchUrl(self, tag):
        h2 = tag.find('h3')
        a = h2.find('a')
        return a.attrs.get('href', '')

    def _findNextPage(self, soup):
        page = -1
        url = ''
        cur = soup.find('td', class_='cur')
        if cur and cur.next_sibling and not cur.next_sibling.get('class'):
            a = cur.next_sibling.find('a')
            page = int(a.text)
            url = urljoin(self.url, a.get('href'))
        return (page, url)
