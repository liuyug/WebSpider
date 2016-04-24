#
# bing: https://msdn.microsoft.com/en-us/library/ff795620.aspx

from .base import EngineBase


class BingEngine(EngineBase):
    def __init__(self, **kwargs):
        super(BingEngine, self).__init__(**kwargs)
        self.name = 'bing'
        self.url = 'http://www.bing.com/search'
        self.page_key = 'first'
        self.search_key = 'q'

    def _format_kv(self, k, v):
        if k == 'inurl':
            if v[0] == '-':
                return '-instreamset:(url):"%s"' % v[1:]
            else:
                return 'instreamset:(url):"%s"' % v
        else:
            return super(BingEngine, self)._format_kv(k, v)

    def _findMatchTags(self, soup):
        return soup.find_all('li', class_='b_algo')

    def _findMatchTitle(self, tag):
        h2 = tag.find('h2')
        return h2.text

    def _findMatchUrl(self, tag):
        h2 = tag.find('h2')
        a = h2.find('a')
        return a.attrs.get('href', '')
