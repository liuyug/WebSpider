
from bs4 import BeautifulSoup
from six.moves.urllib.parse import urlencode

from .. import spider


class EngineSpider(spider.HandlerBase):
    def __init__(self, searching, **kwargs):
        super(EngineSpider, self).__init__(**kwargs)
        self.searching = searching

    def handle(self, data, url):
        soup = BeautifulSoup(data, 'lxml')
        self.searching.handle(soup, url)


class EngineBase(object):
    name = 'base'
    url = None
    page_key = None
    search_key = None
    num_per_page = 10
    pages = None
    search = None
    callbacks = {
        'handleTag': None,
        'handleData': None,
        'handleSoup': None,
    }
    matchs = None
    count = 0

    def __init__(self, **kwargs):
        self.spider = EngineSpider(self, **kwargs)
        self.search = {}
        self.pages = []
        self.matchs = []

    def __str__(self):
        return self.name

    def _format_kv(self, k, v):
        if k == 'text':
            return ' '.join(v)
        elif v[0] == '-':
            return '-%s:%s' % (k, v[1:])
        else:
            return '%s:%s' % (k, v)

    def getEncodeData(self, page=0):
        text = []
        for k, v in self.search.items():
            text.append(self._format_kv(k, v))
        data = {}
        data[self.search_key] = ' '.join(text)
        data[self.page_key] = page * self.num_per_page
        return urlencode(data)

    def getRequestUrl(self, method='GET', page=0):
        if method == 'POST':
            return self.url
        elif method == 'GET':
            return '%s?%s' % (self.url, self.getEncodeData(page=page))
        else:
            raise ValueError('method error: %s' % method)

    def getRequestData(self, method='GET', page=0):
        if method == 'POST':
            return self.getEncodeData(page=page)
        elif method == 'GET':
            return None
        else:
            raise ValueError('method error: %s' % method)

    def addSearch(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'page_max':
                self.pages.extend(range(v))
            elif k == 'page':
                self.pages.append(v)
            elif k == 'text':
                if 'text' not in self.search:
                    self.search['text'] = []
                self.search['text'].extend(v)
            else:
                self.search[k] = v

    def _findMatchTags(self, soup):
        return []

    def _findMatchTitle(self, tag):
        return ''

    def _findMatchUrls(self, tag):
        return ''

    def registerCallback(self,
                         handleData=None,
                         handleTag=None,
                         handleSoup=None):
        if handleData:
            self.callbacks['handleData'] = handleData
        if handleTag:
            self.callbacks['handleTag'] = handleTag
        if handleSoup:
            self.callbacks['handleSoup'] = handleSoup

    def handle(self, soup, url):
        if self.callbacks['handleSoup']:
            self.callbacks['handleSoup'](soup, url)
        for tag in self._findMatchTags(soup):
            if self.callbacks['handleTag']:
                self.callbacks['handleTag'](tag)
            self.count += 1
            data = {
                'title': self._findMatchTitle(tag),
                'url': self._findMatchUrl(tag),
                'index': self.count,
            }
            if self.callbacks['handleData']:
                self.callbacks['handleData'](data)
            self.matchs.append(data)

    def getMatchs(self):
        return self.matchs

    def run_loop(self):
        self.count = 0
        for page in self.pages:
            url = self.getRequestUrl(method='GET', page=page)
            self.spider.put(url)
        self.spider.run_loop()

    def run_once(self):
        self.count = 0
        for page in self.pages:
            url = self.getRequestUrl(method='GET', page=page)
            self.spider.put(url)
        self.spider.run_once()
