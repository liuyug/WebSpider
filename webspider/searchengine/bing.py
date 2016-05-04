#
# bing: https://msdn.microsoft.com/en-us/library/ff795620.aspx

from six.moves.urllib.parse import urljoin
from .base import EngineBase


class BingEngine(EngineBase):
    def __init__(self, **kwargs):
        self.name = 'bing'
        self.firstPage = 'https://www.bing.com/'
        super(BingEngine, self).__init__(**kwargs)
        self.url = 'https://www.bing.com/search'
        self.search_key = 'q'

    def _prefix_word(self, word):
        word = super(BingEngine, self)._prefix_word(word)
        k, _, v = word.partition(':')
        if v and 'inurl' in k:
            kk = k.replace('inurl', 'instreamset:(url)')
            word = '%s:%s' % (kk, v)
        return word

    def _findMatchTags(self, soup):
        return soup.find_all('li', class_='b_algo')

    def _findMatchTitle(self, tag):
        h2 = tag.find('h2')
        return h2.text

    def _findMatchUrl(self, tag):
        h2 = tag.find('h2')
        a = h2.find('a')
        return a.attrs.get('href', '')

    def _findNextPage(self, soup):
        page = -1
        url = ''
        cur_a = soup.find('a', class_='sb_pagS')
        if cur_a:
            cur = cur_a.parent
            if cur and cur.next_sibling:
                a = cur.next_sibling.find('a')
                if not a.get('class'):
                    page = int(a.text)
                    url = urljoin(self.url, a.get('href'))
        return (page, url)
