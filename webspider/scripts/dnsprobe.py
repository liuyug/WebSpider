#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import logging
import argparse

from six.moves.urllib.parse import urlparse
from bs4 import BeautifulSoup

from ..spider import HandlerBase
from ..searchengine import getEngine

version = '0.1.0'
logger = logging.getLogger(__name__)


class SearchDomain(HandlerBase):
    def __init__(self, engine, domain, max_pages=10, agent=None, proxy=None):
        super(SearchDomain, self).__init__(agent=agent, proxy=proxy)
        self.engine = getEngine(engine)
        self.domain = domain
        self.subdomains = []
        for page in range(max_pages):
            self.engine.set_search(search='site:%s -inurl:www' % domain, page=page)
            self.put(self.engine.get_url(), self.engine.get_data())

    def find_urls(self, soup):
        if self.engine.name == 'baidu':
            return soup.find_all('a', class_='c-showurl')
        elif self.engine.name == 'bing':
            return soup.find_all('cite')
        elif self.engine.name == 'google':
            return soup.find_all('cite')
        return []

    def handle(self, data):
        soup = BeautifulSoup(data, 'lxml')
        for tag in self.find_urls(soup):
            parse = urlparse('//%s' % tag.text, scheme='http')
            if (parse.netloc.endswith(self.domain) and
                    parse.netloc not in self.subdomains):
                print(parse.netloc)
                self.subdomains.append(parse.netloc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%%(prog)s %s' % version)
    parser.add_argument('-v', '--verbose', help='verbose help',
                        action='count', default=0)
    parser.add_argument('--user-agent', help='http user agent')
    parser.add_argument('--proxy', help='proxy server, socks5://127.0.0.1:1080')
    parser.add_argument(
        '--engine',
        choices=('baidu', 'bing', 'google'),
        default='baidu',
        help='search engine',
    )
    parser.add_argument('--output', help='output text file')
    parser.add_argument('--max-page', type=int, default=10, help='searching pages')
    parser.add_argument('domain', help='search domain')
    args = parser.parse_args()

    logging.basicConfig(level=(logging.WARNING - args.verbose * 10))

    search_domain = SearchDomain(
        args.engine, args.domain,
        max_pages=args.max_page,
        agent=args.user_agent,
        proxy=args.proxy,
    )
    search_domain.run_once()
    if args.output:
        with open(args.output, 'wb') as f:
            f.write('\n'.join(search_domain.subdomains))


if __name__ == '__main__':
    main()
