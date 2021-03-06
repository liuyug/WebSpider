#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# additional packages:
#   pysocks
#   six
#   lxml
#   BeautifulSoup4

import sys
import codecs
import argparse

import six

from webspider.searchengine import getEngine


version = '0.1.4'
if six.PY2 and not sys.stdout.encoding:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def handleSoup(soup, url):
    print('# page: %s' % url)


def handleData(data):
    global only_url
    if only_url:
        print('%(url)s' % data)
    else:
        text = '# %(index)s.\t%(title)s\n%(url)s' % data
        print(text)


def main():
    epilog = """
Note:
    "-" is prefix character for command line parameter please put "--" in front of "-", such as "-- -inurl:www".

Example:
    %(prog)s --engine baidu <search text>
    %(prog)s --engine baidu site:baidu.com filetype:pdf
    %(prog)s --engine baidu site:baidu.com -- -inurl:www
"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument('--version', action='version',
                        version='%%(prog)s %s' % version)
    parser.add_argument('-v', '--verbose', help='verbose help',
                        action='count', default=0)
    parser.add_argument('--only-url', action='store_true', help='only output url')

    search_group = parser.add_argument_group('Find urls from searching engine')
    search_group.add_argument(
        '--engine',
        choices=('baidu', 'bing', 'google'),
        required=True,
        help='search engine',
    )
    search_group.add_argument('--user-agent', help='http user agent')
    search_group.add_argument('--record-max', type=int, default=30, help='searching max records')
    search_group.add_argument('--proxy', help='proxy server, socks5://127.0.0.1:1080')

    parser.add_argument('content', nargs='+', help='searching content')
    args = parser.parse_args()

    # find urls from searching engine
    if args.engine:
        print('=' * 80)
        engine = getEngine(args.engine, agent=args.user_agent, proxy=args.proxy)
        engine.addSearch(text=args.content)
        engine.addSearch(record_max=args.record_max)
        engine.registerCallback(handleData=handleData, handleSoup=handleSoup)
        global only_url
        only_url = args.only_url

        engine.run_once()


if __name__ == '__main__':
    main()
