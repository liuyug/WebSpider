#
# baidu: http://www.baiduguide.com/baidu-seo-guide/baidu-search-operators/

from six.moves.http_client import HTTPConnection
from six.moves.urllib import parse

from .base import EngineBase


class BaiduEngine(EngineBase):
    def __init__(self, **kwargs):
        super(BaiduEngine, self).__init__(**kwargs)
        self.name = 'baidu'
        self.url = 'http://www.baidu.com/s'
        self.page_key = 'pn'
        self.search_key = 'wd'

    def _findMatchTags(self, soup):
        return soup.find_all('div', class_='c-container')

    def _findMatchTitle(self, tag):
        h3 = tag.find('h3')
        return h3.text.strip() if h3 else ''

    def _findMatchUrl(self, tag):
        h3 = tag.find('h3')
        if not h3:
            return ''
        a = h3.find('a')
        url = a.attrs.get('href', '')
        # decode url
        host = parse.urlsplit(url).netloc
        path = url[len(parse.urljoin(url, '/')) - 1:]
        conn = HTTPConnection(host, timeout=10)
        conn.request('GET', path)
        req = conn.getresponse()
        r_url = req.getheader('Location')
        conn.close()
        return r_url
