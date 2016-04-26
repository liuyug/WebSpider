
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
    firstPage = None
    url = None
    search_key = None
    page_max = None
    search = None
    callbacks = {
        'handleTag': None,
        'handleData': None,
        'handleSoup': None,
    }
    data = None
    matchs = None
    count = 0

    def __init__(self, **kwargs):
        kwargs['cookie'] = self.__getCookie()
        self.spider = EngineSpider(self, **kwargs)
        self.search = {}
        self.matchs = []
        self.data = {}

    def __str__(self):
        return self.name

    def __getCookie(self):
        if self.firstPage:
            ret = spider.url_downloader(self.firstPage)
            if ret['error'] == 'Ok':
                return ret['cookie']
        return None

    def _format_kv(self, k, v):
        if k == 'text':
            return ' '.join(v)
        elif v[0] == '-':
            return '-%s:%s' % (k, v[1:])
        else:
            return '%s:%s' % (k, v)

    def getEncodeData(self):
        text = []
        for k, v in self.search.items():
            text.append(self._format_kv(k, v))
        data = self.data.copy()
        data[self.search_key] = ' '.join(text)
        return urlencode(data)

    def getRequestUrl(self, method='GET'):
        if method == 'POST':
            return self.url
        elif method == 'GET':
            return '%s?%s' % (self.url, self.getEncodeData())
        else:
            raise ValueError('method error: %s' % method)

    def getRequestData(self, method='GET'):
        if method == 'POST':
            return self.getEncodeData()
        elif method == 'GET':
            return None
        else:
            raise ValueError('method error: %s' % method)

    def addSearch(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'page_max':
                self.page_max = v
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

    def _findNextPage(self, soup):
        return (-1, '')

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
        page, next_url = self._findNextPage(soup)
        if next_url and (not self.page_max or page < (self.page_max + 1)):
            self.spider.put(next_url)

    def getMatchs(self):
        return self.matchs

    def run_loop(self):
        self.count = 0
        url = self.getRequestUrl(method='GET')
        self.spider.put(url)
        self.spider.run_loop()

    def run_once(self):
        self.count = 0
        url = self.getRequestUrl(method='GET')
        self.spider.put(url)
        self.spider.run_once()
